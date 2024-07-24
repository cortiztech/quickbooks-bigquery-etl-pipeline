### QuickBooks to Bigquery ETL Pipeline

This repository discusss an ETL pipeline implementation designed to extract data from QuickBooks and feed into a Bigquery table for analytics use. This pipeline is designed to efficiently handle data extraction, transformation and loading processes.

### Overview
The ETL pipeling consists of three main stages.
1. **Extract**: Retrieve QuickBooks raw data using REST API with Oauth2 Authentication.
2. **Load**: Store the extracted data into GCP cloud storage bucket working as the data sink.
3. **Transform**: Utilize dbt to perform transformations from staging to the target Bigquery table.

### Pipeline Workflow
#### 1.Extraction

