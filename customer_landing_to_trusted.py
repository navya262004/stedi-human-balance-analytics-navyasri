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
# Read customer data from Landing zone
# -----------------------------
customer_landing_df = spark.read.json("s3://stedi-landing-navyasri/customer/")

# -----------------------------
# Check schema (optional, for debugging)
# -----------------------------
customer_landing_df.printSchema()
# This will print the exact column names in logs

# -----------------------------
# Filter customers who agreed to research
# -----------------------------
# Use the exact column name from your JSON
customer_trusted_df = customer_landing_df.filter(
    customer_landing_df["shareWithResearchAsOfDate"].isNotNull()
)

# -----------------------------
# Write data to Trusted zone
# -----------------------------
customer_trusted_df.write.mode("overwrite").json(
    "s3://stedi-trusted-navyasri/customer/"
)

# -----------------------------
# Commit the job
# -----------------------------
job.commit()
