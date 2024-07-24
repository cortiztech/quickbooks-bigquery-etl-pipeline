### QuickBooks - Bigquery ETL Pipeline: A Detailed Implementation

#### This repository hosts an ETL pipeline implementation designed to extract data from QuickBooks and feed into a Bigquery table for analytics use.

#### Generally, ETL pipeline is compoesed of extract-load-transform process. The implementation of the stages of the process is described below:
- Extract QuickBooks data using REST API
- Store extracted data into GCP cloud storage bucket working as the data sink
- From cloud storage bucket, utilize dbt to perform transformations from staging to the target Bigquery table.

