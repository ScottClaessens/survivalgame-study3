import boto3
from datetime import datetime

region_name = 'us-east-1'
aws_access_key_id = 'AKIAIN4BVGUYFSPRWGHA'
aws_secret_access_key = '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'

# endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# Uncomment this line to use in production
endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])

# List HITs
response = client.list_hits()
print(response)

# Expire HITs
#response = client.update_expiration_for_hit(
#    HITId='3M4KL7H8KVMCPSULMTABFC71BQT61I',
#    ExpireAt=datetime(2015, 1, 1)
#)
#print(response)

# Delete HITs
#response = client.delete_hit(
#    HITId='3M4KL7H8KVMCPSULMTABFC71BQT61I' # replace with string of current
#)
#print(response)

