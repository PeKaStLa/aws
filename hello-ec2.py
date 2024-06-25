import boto3
import time
from datetime import datetime, timedelta, tzinfo, timezone

def hello_ec2(ec2_resource):
    """
    Use the AWS SDK for Python (Boto3) to create an Amazon Elastic Compute Cloud
    (Amazon EC2) resource and list the security groups in your account.
    This example uses the default settings specified in your shared credentials
    and config files.

    :param ec2_resource: A Boto3 EC2 ServiceResource object. This object is a high-level
                         resource that wraps the low-level EC2 service API.
    """
    print("Hello, Amazon EC2! Let's list up to 10 of your security groups:")
    for sg in ec2_resource.security_groups.limit(10):
        print(f"\t{sg.id}: {sg.group_name}")

    for instance in ec2_resource.instances.limit(10):
        print(f"\t ID: {instance.id} launchtime: {instance.launch_time}")
        
if __name__ == "__main__":
    hello_ec2(boto3.resource("ec2"))


