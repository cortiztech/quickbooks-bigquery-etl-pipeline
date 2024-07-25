### QuickBooks Online to Bigquery ELT Pipeline

This repository discusss an ELT pipeline implementation to extract data from QuickBooks Online and feed into a Bigquery table for analytics use. This pipeline is designed to efficiently handle data extraction, transformation and loading processes.

### Overview
The  pipeline consists of three main stages.
1. **Extract**: Retrieve QuickBooks Online raw data using REST API with Oauth2 Authentication.
2. **Load**: Store the extracted data into GCP cloud storage bucket working as the data sink.
3. **Transform**: Utilize dbt to perform transformations from staging to the target Bigquery table.

### Pipeline Workflow
![image](https://github.com/user-attachments/assets/040be499-7d58-4c83-b380-11e14b83ff9d)

#### 1.Extracti
The extraction stage involves fetching QuickBooks Online raw data using REST API. QBO accounting data includes entities relating to chart of accounts, customers, vendor, products and services, invoices, and other relevant information.

Google Cloud Platform services that is used in the extraction are the following:
1. **Pub/Sub**. Create a Pub/Sub topic to which the cloud function can subscribe.
2. **Cloud Scheduler**. Utilize to setup extraction schedules.
3. **Cloud Function**. Run lightweight code to extract QBO raw data using REST API. This will be triggered by a Pub/Sub topic running on a schedule.

For simplicity of the implementation, a full extraction will be performed everytime. A full extraction is crucial to compare 

#### 2. Load
The loading stage involves storing the raw data in a scalable and secure solution. Google Cloud storage bucket is utilized to serve as a data sink, that is a raw data is stored before it is processed and loaded into the Bigquery data warehouse for analysis.

A key consideration is implemententing an incremental extraction. This means that only new and updated raw data will be extracted and loaded to Google Cloud Storage bucket. This will greatly improve performance and be more resource-efficient.

#### 3. Transform
