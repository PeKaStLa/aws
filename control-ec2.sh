#!/bin/bash


if [[ $1 = "start" ]] && [[ ! -z $2 ]];
then	
	shift
	echo "Start instances: $* now:"
	aws ec2 start-instances --instance-ids $*
	echo "Now waiting for instances to run:"
	aws ec2 wait instance-running --instance-ids $* && echo "All Instances are running now." || echo "Something went wrong with the wait-cmd."
fi


if [[ $1 = "stop" ]] && [[ ! -z $2 ]];
then	
	shift
	echo "Stop instances: $* now:"
	aws ec2 stop-instances --instance-ids $*
	echo "Now waiting for instances to stop:"
	aws ec2 wait instance-stopped --instance-ids $*  && echo "All Instances are stopped now." || echo "Something went wrong with the wait-cmd."
fi


if [[ $1 = "start" ]] && [[ -z $2 ]]; then
	output_all_stopped_instances=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=stopped | jq -r '.Reservations[].Instances[].InstanceId' | tr '\n' ' ' | tr -d '\r' | cat -v)
	if [[ ! -z $output_all_stopped_instances ]]; 
	then
		echo "Starting all instances now: $output_all_stopped_instances"
		aws ec2 start-instances --instance-ids $output_all_stopped_instances 
		echo "Now waiting for instances to run:"
		aws ec2 wait instance-running --instance-ids $output_all_stopped_instances && echo "All Instances are running now." || echo "Something went wrong with the wait-cmd."
	else
		echo "No stopped instances to start."
	fi
fi


if [[ $1 = "stop" ]] && [[ -z $2 ]]; then
	output_all_running_instances=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=running | jq -r '.Reservations[].Instances[].InstanceId' | tr '\n' ' ' | tr -d '\r' | cat -v)
	if [[ ! -z $output_all_running_instances ]]; 
	then
		echo "Stopping all instances now: $output_all_running_instances"
		aws ec2 stop-instances --instance-ids $output_all_running_instances
		echo "Now waiting for instances to stop:"
		aws ec2 wait instance-stopped --instance-ids $output_all_running_instances  && echo "All Instances are stopped now." || echo "Something went wrong with the wait-cmd."
	else
		echo "No running instances to stop."
	fi
fi


if [[ $1 = "status" ]] && [[ -z $2 ]];
then
	echo "List all instance-statuses now:"
	output_all_statuse=$(aws ec2 describe-instances | jq -r '.Reservations[].Instances[]  | "\(.InstanceId) is \(.State.Name)"')
	if [[ ! -z $output_all_statuse ]]; 
	then
		echo "$output_all_statuse"
	else
		echo "No instances to list."
	fi
fi


if [[ $1 = "status" ]] && [[ ! $2 = "stopped" ]] && [[ ! $2 = "running" ]] && [[ ! -z $2 ]];
then	
	echo "Show status of instance: $2 now:"
	aws ec2 describe-instance-status --instance-ids $2  | jq -r '.InstanceStatuses.[].InstanceState.Name '
fi


if [[ $1 = "status" ]] && [[ $2 = "stopped" ]];
then
	echo "Show all stopped instances now:"
	output_all_stopped_instances=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=stopped | jq -r '.Reservations[].Instances[].InstanceId')
	if [[ ! -z $output_all_stopped_instances ]]; 
	then
		echo "$output_all_stopped_instances"
	else
		echo "No instances are stopped."
	fi
fi


if [[ $1 = "status" ]] && [[ $2 = "running" ]];
then 
	echo "Show all running instances now:"
	output_all_running_instances=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=running | jq -r '.Reservations[].Instances[].InstanceId')
	if [[ ! -z $output_all_running_instances ]]; 
	then
		echo "$output_all_running_instances"
	else
		echo "No instances are running."
	fi
fi


# empty Dollar1
if [[ -z $1 ]];
then
	echo -e "Usage: \ncontrol-ec2.sh ['status'|'start'|'stop'] ['stopped'|'running'|<instance-id>]"
	echo -e "Examples: \ncontrol-ec2.sh status \ncontrol-ec2.sh status running"
	echo -e "control-ec2.sh start \ncontrol-ec2.sh stop i-059604ca3cf21bc80"
fi


# unknown Dollar1
if [[ ! -z $1 ]] && [[ ! $1 = "status" ]] && [[ ! $1 = "start" ]] && [[ ! $1 = "stop" ]];
then
	echo "Unknown Dollar1. Use without Parameters to see instructions on usage."
fi

