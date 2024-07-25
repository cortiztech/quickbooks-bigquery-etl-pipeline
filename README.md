### QuickBooks Online to Bigquery ELT Pipeline

This repository discusses an ELT pipeline implementation to extract data from QuickBooks Online and feed it into a Bigquery table for analytics use. This pipeline is designed to efficiently handle data extraction, load to a data sink, and transformation based on business requirements.

### Overview
The  pipeline consists of three main stages.
1. **Extract**: Retrieve QuickBooks Online raw data using REST API with Oauth2 Authentication.
2. **Load**: Store the extracted data in the GCP cloud storage bucket as the data sink.
3. **Transform**: Utilize dbt to perform transformations from staging to the target Bigquery table.

### Pipeline Workflow
![image](https://github.com/user-attachments/assets/543289e4-d5eb-4ff9-ac99-db9c5da10cf5)


#### 1. Extract
The extraction stage involves fetching QuickBooks Online raw data using REST API. QBO accounting data includes entities related to chart of accounts, customers, vendors, products and services, invoices, and other relevant information.

Google Cloud Platform services that are used in the extraction are the following:
1. **Pub/Sub**. Create a Pub/Sub topic to which the cloud function can subscribe.
2. **Cloud Scheduler**. Utilize to set up extraction schedules.
3. **Cloud Function**. Run lightweight code to extract QBO raw data using REST API. This will be triggered by a Pub/Sub topic running on a schedule.

For simplicity of the implementation, a full extraction will be performed every time. 

Another possible implementation is incremental extraction, where only the new and updated records are loaded into the data sink. Additionally, others may work on an extraction process that implements Change Data Capture (CDC) to account for all new, updated, and deleted records since the last extraction.

#### 2. Load
The loading stage involves storing the raw data in a scalable and secure solution. Google Cloud storage bucket is utilized to serve as a data sink to enable to storage of raw data before it is processed and loaded into the Bigquery data warehouse for analysis.


#### 3. Transform
