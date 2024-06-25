import json
import boto3
from datetime import datetime, timedelta, timezone

import os
import smtplib
from email.message import EmailMessage
from botocore.exceptions import ClientError
from botocore.vendored import requests

print("start")

def send_mail(info):
    
    print("Start. Sending Mail now.")
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Peter Karl Stadler <peter.stadler@stadlersoft.de>"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "14peterstadler@gmail.com"
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-central-1"
    
    # The subject line for the email.
    SUBJECT = "FINAL - Eine ec2-Instanz war zu lange online und wurde gestoppt"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ( info )

                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>"Eine ec2-Instanz war zu lange online und wurde gestoppt."</h1>
      <p>"Eine ec2-Instanz war zu lange online und wurde gestoppt."</p>
    </body>
    </html>
                """            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        
    print("End. Mail sent.")
    
    

def lambda_handler(event, context):
    
    ec2_resource=boto3.resource("ec2")
    ec2_client = boto3.client("ec2")

    for instance in ec2_resource.instances.limit(100):
        
        print(f"\t #################################### \nID: {instance.id} launchtime: {instance.launch_time}")
        print("instance.state: ", instance.state)
        instance_launchtime=datetime.fromisoformat(str(instance.launch_time))
        instance_launchtime_plus=instance_launchtime + timedelta(hours=5)
        # instance_launchtime_plus=instance_launchtime + timedelta(minutes=20)
        nowutc=datetime.now(timezone.utc)
        print("instance_launchtime + x-hours : ", instance_launchtime_plus )  
        print("nowutc: ", nowutc)  
        
        if str(instance.state) == "{'Code': 16, 'Name': 'running'}" and nowutc > instance_launchtime_plus:
            print("Instance-state is running and time now-utc is greater than the treshold, which means the instance runs more than x-hours and should be stopped.")
            print("Try stopping the instance: ", instance.id)
            response = ec2_client.stop_instances(
                InstanceIds=[
                    str(instance.id),
                ]
            )
            print(response)
            send_mail("InstanceID: " + str(instance.id) + ", LaunchTime: " + str(instance.launch_time) + ", Instance.state: " + str(instance.state) )
           
        else:
            print("Instance-state is not running and/or time now-utc is smaller than the treshold, which means the instance was just started and runs less than x-hours.")

            
    print("end")

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('hmmm!')
    }