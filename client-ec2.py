import boto3

ec2 = boto3.client('ec2')

response = ec2.stop_instances(
    InstanceIds=[
        'i-01d36722a40600908',
    ]
)

print(response)
