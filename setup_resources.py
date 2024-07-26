import json
from google.cloud import storage, bigquery
from google.cloud import pubsub_v1
from googleapiclient import discovery
from google.oauth2 import service_account

# Load configuration
with open('config/config.json') as config_file:
    config = json.load(config_file)

project_id = config['project_id']
bucket_name = config['bucket_name']
topic_name = config['topic_name']
job_name = config['job_name']
schedule = config['schedule']
dataset_name = config['dataset_name']
service_account_path = config['service_account_path']

# Authenticate and create credentials
credentials = service_account.Credentials.from_service_account_file(service_account_path)

storage_client = storage.Client(credentials=credentials, project=project_id)
bigquery_client = bigquery.Client(credentials=credentials, project=project_id)
pubsub_client = pubsub_v1.PublisherClient(credentials=credentials)
scheduler_service = discovery.build('cloudscheduler', 'v1', credentials=credentials)

def create_bucket():
    """Create a new bucket for extracted QuickBooks raw data."""
    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        bucket.storage_class = 'STANDARD'
        bucket.location = 'US'
        bucket.create()
        print(f'Bucket {bucket.name} created')
    else:
        print(f'Bucket {bucket.name} already exists')

def create_topic():
    """Create a new Pub/Sub topic."""
    topic_path = pubsub_client.topic_path(project_id, topic_name)
    try:
        topic = pubsub_client.create_topic(name=topic_path)
        print(f'Topic {topic.name} created')
    except Exception as e:
        print(f'Failed to create topic: {e}')

def create_scheduler_job():
    """Create a new Cloud Scheduler job."""
    location = 'us-central1'
    parent = f'projects/{project_id}/locations/{location}'
    job = {
        'name': f'{parent}/jobs/{job_name}',
        'pubsubTarget': {
            'topicName': f'projects/{project_id}/topics/{topic_name}',
            'attributes': {
                'schedule': schedule,
                'data': ''
            }
        },
        'schedule': schedule,
        'timeZone': 'UTC'
    }
    try:
        response = scheduler_service.projects().locations().jobs().create(parent=parent, body=job).execute()
        print(f'Job {response["name"]} created')
    except Exception as e:
        print(f'Failed to create job: {e}')

def create_dataset():
    """Create a new BigQuery dataset."""
    dataset_id = f'{project_id}.{dataset_name}'
    dataset = bigquery.Dataset(dataset_id)
    try:
        dataset = bigquery_client.create_dataset(dataset)
        print(f'Dataset {dataset.dataset_id} created')
    except Exception as e:
        print(f'Failed to create dataset: {e}')

if __name__ == '__main__':
    create_bucket()
    create_topic()
    create_scheduler_job()
    create_dataset()
