### QuickBooks Online to Bigquery ETL Pipeline

This repository discusss an ETL pipeline implementation to extract data from QuickBooks Online and feed into a Bigquery table for analytics use. This pipeline is designed to efficiently handle data extraction, transformation and loading processes.

### Overview
The ETL pipeling consists of three main stages.
1. **Extract**: Retrieve QuickBooks Online raw data using REST API with Oauth2 Authentication.
2. **Load**: Store the extracted data into GCP cloud storage bucket working as the data sink.
3. **Transform**: Utilize dbt to perform transformations from staging to the target Bigquery table.

### Pipeline Workflow
#### 1.Extraction
The extraction stage involves fetching QuickBooks Online raw data using REST API. QBO accounting data includes entities relating to chart of accounts, customers, vendor, products and services, invoices, and other relevant information.

Google Cloud Platform services that is used in the extraction are the following:
1. **Pub/Sub**. Create a Pub/Sub topic to which the cloud function can subscribe.
2. **Cloud Scheduler**. Utilize to setup extraction schedules.
3. **Cloud Function**. Run lightweight code to extract QBO raw data using REST API. This will be triggered by a Pub/Sub topic running on a schedule.
