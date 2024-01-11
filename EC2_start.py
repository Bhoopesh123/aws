import boto3
region = 'us-east-1'
instances = ['i-0a60108271aaf315e']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('Start your instances: ' + str(instances))