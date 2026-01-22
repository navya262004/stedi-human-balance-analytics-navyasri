# Project: STEDI-Human-Balance-Analytics

## Contents

+ [Problem Statement](#Problem-Statement)
+ [Project Discription](#Project-Discription)
+ [Project Datasets](#Project-Datasets)
+ [Implementation](#Implementation)


---
## Problem Statement

The STEDI Team has been hard at work developing a hardware STEDI Step Trainer that:
- trains the user to do a STEDI balance exercise
- has sensors on the device that collect data to train a machine-learning algorithm to detect steps
- has a companion mobile app that collects customer data and interacts with the device sensors

STEDI has heard from millions of early adopters who are willing to purchase the STEDI Step Trainers and use them.

Several customers have already received their Step Trainers, installed the mobile application, and begun using them together to test their balance. The Step Trainer is just a motion sensor that records the distance of the object detected. The app uses a mobile phone accelerometer to detect motion in the X, Y, and Z directions.

The STEDI team wants to use the motion sensor data to train a machine learning model to detect steps accurately in real-time. Privacy will be a primary consideration in deciding what data can be used.

Some of the early adopters have agreed to share their data for research purposes. Only these customers’ Step Trainer and accelerometer data should be used in the training data for the machine learning model.

---

### Project Discription

In this project I extracted data produced by the STEDI Step Trainer sensors and the mobile app, and curated them into a data lakehouse solution on AWS. The intent is for Data Scientists to use the solution to train machine learning models. 

The Data lake solution is developed using AWS Glue, AWS S3, Python, and Spark for sensor data that trains machine learning algorithms.

AWS infrastructure is used to create storage zones (landing, trusted and curated), data catalog, data transformations between zones and queries in semi-structured data.

---

## Project Datasets

* Customer Records: from fulfillment and the STEDI website.  
* Step Trainer Records: data from the motion sensor.
* Accelerometer Records: data from the mobile app.

---

## Implementation

<details>
<summary>
Landing Zone
</summary>

> In the Landing Zone, raw customer, accelerometer, and step trainer data are stored in AWS S3. AWS Glue Data Catalog is used to create tables for querying via Athena.

**Landing Tables and Screenshots:**

1- **Customer Landing Table:**  
![Customer Landing](screenshots_outputs/customer_landing.png)

2- **Accelerometer Landing Table:**  
![Accelerometer Landing](screenshots_outputs/accelerometer_landing.png)

3- **Step Trainer Landing Table:**  
![Step Trainer Landing](screenshots_outputs/step_trainer_landing.png)

</details>

<details>
<summary>
Trusted Zone
</summary>

> In the Trusted Zone, AWS Glue jobs transform raw data from the landing tables to trusted tables.

**Glue Job Scripts:**

1. [`customer_landing_to_trusted.py`](customer_landing_to_trusted.py) – Transfers customer data from landing → trusted, filtering for customers who agreed to share data.  

2. [`accelerometer_landing_to_trusted.py`](accelerometer_landing_to_trusted.py) – Transfers accelerometer data from landing → trusted, filtering for readings from customers who agreed to share data.  

3. [`trainer_landing_to_trusted.py`](trainer_landing_to_trusted.py) – Transfers Step Trainer data from landing → trusted, filtering for customers with accelerometer readings who agreed to share data.  

**Trusted Tables and Screenshots:**

- Customer Trusted Table:  
![Customer Trusted](screenshots_outputs/customer_trusted.png)  

- Customer Trusted with Null Timestamps (Shared for Research):  
![Customer Trusted Research](screenshots_outputs/customer_trusted_sharwithreasearchasofdate_null.png)  

- Accelerometer Trusted Table:  
![Accelerometer Trusted](screenshots_outputs/accelerometer_trusted.png)  

- Step Trainer Trusted Table:  
![Step Trainer Trusted](screenshots_outputs/step_trainer_trusted.png)

</details>

<details>
<summary>
Curated Zone
</summary>

> In the Curated Zone, AWS Glue jobs make further transformations to produce analysis-ready datasets.

**Glue Job Scripts:**

1. [`customer_trusted_to_curated.py`](customer_trusted_to_curated.py) – Transfers customer data from trusted → curated, filtering for customers with accelerometer readings who agreed to share data.  

2. [`trainer_trusted_to_curated.py`](trainer_trusted_to_curated.py) – Builds aggregated tables combining Step Trainer readings and associated accelerometer readings for the same timestamp, only for customers who agreed to share data.  

**Curated Tables and Screenshots:**

- Customer Curated Table:  
![Customer Curated](screenshots_outputs/customer_curated.png)  

- ML Curated Dataset:  
![ML Curated](screenshots_outputs/ml_curated.png)

</details>
