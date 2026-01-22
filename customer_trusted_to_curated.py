import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# -----------------------------
# Job setup
# -----------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -----------------------------
# Read trusted datasets
# -----------------------------
customer_df = spark.read.json("s3://stedi-trusted-navyasri/customer/")
accelerometer_df = spark.read.json("s3://stedi-trusted-navyasri/accelerometer/")
step_trainer_df = spark.read.json("s3://stedi-trusted-navyasri/step_trainer/")

# -----------------------------
# Join customer with accelerometer
# customer.serialnumber = accelerometer.user
# -----------------------------
cust_accel_df = customer_df.join(
    accelerometer_df,
    customer_df["serialnumber"] == accelerometer_df["user"],
    "inner"
)

# -----------------------------
# Join with step trainer
# customer.serialnumber = step_trainer.serialnumber
# -----------------------------
customer_curated_df = cust_accel_df.join(
    step_trainer_df,
    cust_accel_df["serialnumber"] == step_trainer_df["serialnumber"],
    "inner"
).select(customer_df["*"]).dropDuplicates()

# -----------------------------
# Write curated customer data
# -----------------------------
customer_curated_df.write.mode("overwrite").json(
    "s3://stedi-curated-navyasri/customer/"
)

job.commit()
