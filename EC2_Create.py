import json
import boto3
import botocore.exceptions
import traceback

def lambda_handler(event, context):
    # Default region
    region = "us-east-1"
    instance_type = None

    # ⚠️ Ensure this AMI exists in ap-south-1
    ami_id = "ami-0ecb62995f68bb549"

    print("Received Event:\n", json.dumps(event, indent=2))

    try:
        action_group = event.get("actionGroup", "")
        invoked_function = event.get("function", "")
        session_attributes = event.get("sessionAttributes", {})
        prompt_session_attributes = event.get("promptSessionAttributes", {})
        parameters = event.get("parameters", [])

        # 🔍 DEBUG: log incoming parameters
        print("Received parameters:")
        for param in parameters:
            print(f" - {param.get('name')} = {param.get('value')}")

        # ✅ FIX: accept both snake_case and hyphen
        for param in parameters:
            name = param.get("name")
            value = param.get("value")

            if name == "region":
                region = value
            elif name in ["instance_type", "instance-type"]:
                instance_type = value

        if not instance_type:
            raise ValueError("Missing required parameter: instance_type")

        ec2 = boto3.client("ec2", region_name=region)

        print(
            f"Creating EC2 instance | Region: {region} | "
            f"InstanceType: {instance_type} | AMI: {ami_id}"
        )

        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1
        )

        instance_id = response["Instances"][0]["InstanceId"]
        print(f"Instance launched: {instance_id}")

        waiter = ec2.get_waiter("instance_running")
        waiter.wait(InstanceIds=[instance_id])

        describe = ec2.describe_instances(InstanceIds=[instance_id])
        instance = describe["Reservations"][0]["Instances"][0]
        public_ip = instance.get("PublicIpAddress", "No public IP assigned")

        payload = {
            "instanceId": instance_id,
            "publicIpAddress": public_ip,
            "region": region
        }

        bedrock_response = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": action_group,
                "function": invoked_function,
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(payload)
                        }
                    }
                }
            },
            "sessionAttributes": session_attributes,
            "promptSessionAttributes": prompt_session_attributes
        }

        print("Returning success response:\n", json.dumps(bedrock_response, indent=2))
        return bedrock_response

    except ValueError as e:
        print("Parameter error:", str(e))

        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup", ""),
                "function": event.get("function", ""),
                "functionResponse": {
                    "responseState": "REPROMPT",
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"errorMessage": str(e)})
                        }
                    }
                }
            }
        }

    except botocore.exceptions.ClientError as e:
        print("AWS error:", str(e))
        traceback.print_exc()

        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup", ""),
                "function": event.get("function", ""),
                "functionResponse": {
                    "responseState": "FAILURE",
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({
                                "errorMessage": e.response["Error"]["Message"]
                            })
                        }
                    }
                }
            }
        }

    except Exception as e:
        print("Unexpected error:", str(e))
        traceback.print_exc()

        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup", ""),
                "function": event.get("function", ""),
                "functionResponse": {
                    "responseState": "FAILURE",
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"errorMessage": str(e)})
                        }
                    }
                }
            }
        }
