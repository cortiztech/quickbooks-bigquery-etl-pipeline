 import json
from google.cloud import storage, bigquery, pubsub_v1
from googleapiclient import discovery
from oauth2client import service_account

#Load configuration
with open('config/config.json') as f:
    config = json.load(f)

project_id = config['project_id']
bucket_name = config['bucket_name']
topic_name = config['topic_name']
job_name = config['job_name']
schedule = config['schedule']
dataset_name = config['dataset_name']
service_account_path = config['service_account_path']

#Authenticate and create credentials
credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(service_account_path)
storage_client = storage.Client(credentials=credentials)
bigquery_client = bigquery.Client(credentials=credentials)
pubsub_client = pubsub_v1.PublisherClient(credentials=credentials)
scheduler_service = discovery.build('scheduler', 'v1', credentials=credentials)


def create_bucket():
   """Create a new bucket for extracted QuickBooks raw data."""
   bucket = storage_client.bucket(bucket_name)
   if not bucket.exists():
        bucket.storage_class = 'STANDARD'
        bucket.location = 'US'
        bucket.create()
        print('Bucket {} created'.format(bucket.name))
   else:
    print('Bucket {} already exists'.format(bucket.name))

def create_topic(topic_name):
    """Create a new Pub/Sub topic."""
    topic_path = pubsub_client.topic_path(project_id, topic_name)
    try:
        topic = pubsub_client.create_topic(topic_path)
        print('Topic {} created'.format(topic.name))
    except Exception as e:
        print(f'Failed to create topic: {e}')
    
def create_scheduler(job_name, schedule, topic_name):
    """Create a new Cloud Scheduler job."""
    location = 'us-central1'
    parent = f'projects/{project_id}/locations/{location}'
    job = {
        'name': f'projects/{project_id}/locations/{location}/jobs/{job_name}',
        'pubsubTarget': {
            'topicName': f'projects/{project_id}/topics/{topic_name}',
            'attributes': {
                'schedule': schedule,
            'data': ''
            }
        }
    }
    try:
        response = scheduler_service.projects().locations().jobs().create(parent=parent, body=job).execute()
        print(f'Job {response["name"]} created')
    except Exception as e:
        print(f'Failed to create job: {e}')

def create_dataset(dataset_name):
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
    create_topic(topic_name)
    create_scheduler(job_name, schedule, topic_name)
    create_dataset(dataset_name)

