import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# -----------------------------
# Read job arguments
# -----------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# -----------------------------
# Create Spark and Glue contexts
# -----------------------------
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -----------------------------
# Read accelerometer data from Landing zone
# -----------------------------
accelerometer_df = spark.read.json("s3://stedi-landing-navyasri/accelerometer/")

# -----------------------------
# Optional: Check schema
# -----------------------------
accelerometer_df.printSchema()

# -----------------------------
# Write data to Trusted zone
# -----------------------------
# No filtering needed for accelerometer
accelerometer_df.write.mode("overwrite").json(
    "s3://stedi-trusted-navyasri/accelerometer/"
)

# -----------------------------
# Commit the job
# -----------------------------
job.commit()
