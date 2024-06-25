import boto3
from datetime import datetime, timedelta, tzinfo, timezone

def main():

    ec2_resource=boto3.resource("ec2")
    ec2_client = boto3.client("ec2")

    for instance in ec2_resource.instances.limit(100):
        print(f"\t #################################### \nID: {instance.id} launchtime: {instance.launch_time}")
        instance_launchtime=datetime.fromisoformat(str(instance.launch_time))
        instance_launchtime_plus=instance_launchtime + timedelta(hours=8)
        # instance_launchtime_plus=instance_launchtime + timedelta(minutes=10)
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
        else:
            print("Instance-state is not running and/or time now-utc is smaller than the treshold, which means the instance was just started and runs less than x-hours.")


if __name__ == "__main__":
    main()


