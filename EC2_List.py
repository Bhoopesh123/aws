import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    # Ensure Lambda role has ec2:DescribeInstances permission

    # Log the event received - vital for checking 'function' vs 'apiPath' etc.
    print("Received Event: ", json.dumps(event))

    try:
        # --- Extract details from event ---
        # For "Function Details" method, expect 'function' key from the event
        action_group = event.get('actionGroup', '')
        invoked_function = event.get('function', '') # Use the 'function' key from the event
        session_attributes = event.get('sessionAttributes', {})
        prompt_session_attributes = event.get('promptSessionAttributes', {})

        # --- Core Logic: List EC2 Instances ---
        instance_ids = []
        paginator = ec2.get_paginator('describe_instances')
        # Adjust filters as needed
        page_iterator = paginator.paginate(Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running', 'shutting-down', 'stopping', 'stopped']}])

        for page in page_iterator:
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    instance_ids.append(instance['InstanceId'])
        # --- End Core Logic ---

        # --- Prepare the Payload ---
        # This structure MUST implicitly match how you described the function's
        # return value in the Bedrock console's "Function Details" section.
        payload = {
            "instanceIds": instance_ids,
            "count": len(instance_ids)
        }
        print("Payload Dictionary:", payload)

        # Stringify the payload - Bedrock expects the body as a string
        stringified_payload_body = json.dumps(payload)
        print("Stringified Payload Body:", stringified_payload_body)
        # --- End Prepare the Payload ---

        # --- Construct the innermost responseBody map ---
        # Use 'application/json' for structured data. Change if you defined
        # a different return content type (e.g., 'text/plain') in Bedrock.
        content_type = 'TEXT'
        response_body_map = {
            content_type: {
                'body': stringified_payload_body
            }
        }
        # --- End Construct the innermost responseBody map ---

        # --- Construct the functionResponse object ---
        # This contains the responseBody map, as per docs.
        function_response_part = {
            'responseBody': response_body_map
        }
        # --- End Construct the functionResponse object ---

        # --- Assemble the main 'response' object ---
        # Use 'function' key matching the event, and nest 'functionResponse'
        agent_response_part = {
            'actionGroup': action_group,
            'function': invoked_function, # Mirror the 'function' key from the event
            'functionResponse': function_response_part # Embed the nested structure
        }
        # --- End Assemble the main 'response' object ---

        # --- Build the final return object ---
        bedrock_response = {
            'messageVersion': '1.0',
            'response': agent_response_part,
            'sessionAttributes': session_attributes,
            'promptSessionAttributes': prompt_session_attributes
        }
        # --- End Build the final return object ---

        print("Returning Bedrock Response: ", json.dumps(bedrock_response))
        return bedrock_response

    except Exception as e:
        print(f"Error processing event: {str(e)}", exc_info=True) # Log full traceback

        # Construct error response following the structure as best as possible
        error_payload = {'errorMessage': str(e)}
        # Determine the key ('function' or 'apiPath') based on what was likely in the event
        invoked_identifier = event.get('function') or event.get('apiPath', 'N/A')
        error_response_key = 'function' if event.get('function') else 'apiPath'

        error_body_map = {
            'application/json': { # Assuming error is also JSON
                 'body': json.dumps(error_payload)
            }
        }
        error_function_response = {'responseBody': error_body_map}

        error_agent_response = {
             'actionGroup': event.get('actionGroup', 'N/A'),
             error_response_key: invoked_identifier, # Use the identified key
             'functionResponse': error_function_response
        }

        return {
            'messageVersion': '1.0',
            'response': error_agent_response,
            'sessionAttributes': event.get('sessionAttributes', {}),
            'promptSessionAttributes': event.get('promptSessionAttributes', {})
        }
