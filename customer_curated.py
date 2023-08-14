import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-project-udacity/customer_trusted/"],
        "recurse": True,
    },
    transformation_ctx="S3bucket_node1",
)

# Script generated for node Amazon S3
AmazonS3_node1692030001186 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-project-udacity/accelerometer_landing/"],
        "recurse": True,
    },
    transformation_ctx="AmazonS3_node1692030001186",
)

# Script generated for node Join Privacy
JoinPrivacy_node1692030024964 = Join.apply(
    frame1=S3bucket_node1,
    frame2=AmazonS3_node1692030001186,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="JoinPrivacy_node1692030024964",
)

# Script generated for node Drop Fields
DropFields_node1692030682958 = DropFields.apply(
    frame=JoinPrivacy_node1692030024964,
    paths=["user", "timeStamp", "x", "y", "z"],
    transformation_ctx="DropFields_node1692030682958",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1692030682958,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-project-udacity/customer_curated/",
        "partitionKeys": [],
    },
    transformation_ctx="S3bucket_node3",
)

job.commit()
