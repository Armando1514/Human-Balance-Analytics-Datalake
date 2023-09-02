# Human Balance Lakehouse

![datalake](./img/lakehouse.png)

Using AWS Glue, AWS S3, Python, and Spark, create or generate Python  scripts to build a lakehouse solution in AWS that satisfies these  requirements from the STEDI data scientists. Project required from AWS Data Engineering nanodegree on Udacity.

## STACK

- Python and Spark
- AWS Glue
- AWS Athena
- AWS S3

## DATA FOLDER (LANDING ZONES)

To simulate the data coming from the various sources, you will need to  create your own S3 directories for  customer_landing,  step_trainer_landing, and accelerometer_landing, and copy the data folder there as a starting point.

### **1. Customer Records**

Contains the following fields:

- serialnumber
- sharewithpublicasofdate
- birthday
- registrationdate
- sharewithresearchasofdate
- customername
- email
- lastupdatedate
- phone
- sharewithfriendsasofdate

### **2. Step Trainer Records (data from the motion sensor):**

Contains the following fields:

- sensorReadingTime
- serialNumber
- distanceFromObject

### **3. Accelerometer Records (from the mobile app):**

Contains the following fields:

- timeStamp
- user
- x
- y
- z

There are  **two Glue tables** for the two landing zones: customer_landing.sql and accelerometer_landing.sql.

This is how it looks like customer_landing and accelerometer_landing querying them with **AWS Athena**:

![customer_landing](./img/customer_landing.png)

![accelerometer_landing](./img/accelerometer_landing.png)

## TRUSTED AND CURATED ZONES

The Data Science team has done some preliminary data analysis and determined that the **Accelerometer Records** each match one of the **Customer Records**. They would like you to create 2 AWS Glue Jobs that do the following:

1. Sanitize the  Customer data from the Website (Landing Zone) and only store the  Customer Records who agreed to share their data for research purposes  (Trusted Zone) - creating a Glue Table called **customer_trusted** (customer_trusted.py). Below the query from Athena of the customer_trusted s3 bucket:![customer_trusted](./img/customer_trusted.png)

   A screenshot that shows a select * statement from Athena showing the  customer landing data, where the resulting customer trusted data has no  rows where shareWithResearchAsOfDate is blank.

   ![customer_trusted_blank](./img/customer_trusted_blank.png)

2. Sanitize the Accelerometer data from the Mobile App (Landing Zone) - and only  store Accelerometer Readings from customers who agreed to share their  data for research purposes (Trusted Zone) - creating a Glue Table called **accelerometer_trusted**. Below the query from Athena of the accelerometer_trusted s3 bucket:![accelerometer_trusted](./img/accelerometer_trusted.png)

**NOTE**:

For AWS Glue to act on your behalf to  access S3 and other resources, you need to grant access to the Glue  Service by creating an IAM Service Role that can be assumed by Glue:

```
aws iam create-role --role-name my-glue-service-role --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'
```

Data Scientists have discovered a data quality issue with the Customer Data. The serial number should be a  unique identifier for the STEDI Step Trainer they purchased. However,  there was a defect in the fulfillment website, and it used the same 30  serial numbers over and over again for millions of customers!  Most  customers have not received their Step Trainers yet, but those who have, are submitting Step Trainer data over the IoT network (Landing Zone). *The data from the Step Trainer Records has the correct serial numbers.*

The problem is that because of this  serial number bug in the fulfillment data (Landing Zone), we don’t know  which customer the Step Trainer Records data belongs to.

The Data Science team would like you to write a Glue job that does the following:

3. Sanitize the  Customer data (Trusted Zone) and create a Glue Table (Curated Zone) that only includes customers who have accelerometer data *and* have agreed to share their data for research called **customer_curated** (customer_curated.py).

Finally, you need to create two Glue Studio jobs that do the following tasks:

4. Read the Step Trainer IoT data stream (S3) and populate a Trusted Zone Glue Table called **step_trainer_trusted** that contains the Step Trainer Records data for customers who have  accelerometer data and have agreed to share their data for research  (customer_curated). Look for it step_trainer_trusted.py

5. Create an aggregated  table that has each of the Step Trainer Readings, and the associated  accelerometer reading data for the same timestamp, but only for  customers who have agreed to share their data, and make a glue table  called **machine_learning_curated.** You can find it in machine_learning_curated.py