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
# Read step trainer data from Landing zone
# -----------------------------
step_trainer_df = spark.read.json("s3://stedi-landing-navyasri/step_trainer/")

# -----------------------------
# Optional: Check schema
# -----------------------------
step_trainer_df.printSchema()

# -----------------------------
# Write data to Trusted zone
# -----------------------------
# No filtering needed for step trainer
step_trainer_df.write.mode("overwrite").json(
    "s3://stedi-trusted-navyasri/step_trainer/"
)

# -----------------------------
# Commit the job
# -----------------------------
job.commit()
