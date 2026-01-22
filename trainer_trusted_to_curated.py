import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# ------------------------------------------------
# Job setup
# ------------------------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ------------------------------------------------
# Read trusted datasets
# ------------------------------------------------
step_trainer_df = spark.read.json("s3://stedi-trusted-navyasri/step_trainer/")
accelerometer_df = spark.read.json("s3://stedi-trusted-navyasri/accelerometer/")

# ------------------------------------------------
# (Optional) Print schemas for confirmation
# ------------------------------------------------
step_trainer_df.printSchema()
accelerometer_df.printSchema()

# ------------------------------------------------
# Join step trainer with accelerometer
# Correct join keys:
# step_trainer.sensorReadingTime = accelerometer.timeStamp
# ------------------------------------------------
ml_curated_df = step_trainer_df.join(
    accelerometer_df,
    step_trainer_df["sensorReadingTime"] == accelerometer_df["timeStamp"],
    "inner"
)

# ------------------------------------------------
# Write Machine Learning curated dataset
# ------------------------------------------------
ml_curated_df.write.mode("overwrite").json(
    "s3://stedi-curated-navyasri/machine_learning_curated/"
)

job.commit()
