# EC2 Automatic Start and Stop using Lambda

Kindly follow the below steps to create EC2 Instance(Windows and Linux) creation on AWS Cloud

# 1. IAM Policy Creation

Sign in to the AWS Management Console and open the IAM console at 
https://console.aws.amazon.com/iam/.

    In the navigation pane on the left, choose Policies.
    Choose Create policy.
    In the Policy editor section, choose the JSON option.
    Paste a JSON(IAM_Policy.json)
    Give the name as "Start_Stop_EC2"
    Chose Next and Create the policy

# 2. IAM Role

Sign in to the AWS Management Console and open the IAM console at 
https://console.aws.amazon.com/iam/.

    In the navigation pane of the IAM console, choose Roles, and then choose Create role.
    For Trusted entity type, choose AWS service.
    For Service or use case, choose a service, and then choose the use case. Use cases are defined by the service to include the trust policy that the service requires.
    Choose Next.
    For Permissions policies, the options depend on the use case that you selected:
    Chose Next and Create the Role

# 3. Lambda EC2 Stop Function

Open the Lambda console, 

    Choose Create function.
    Choose Author from scratch.
    Under Basic information, enter the following information:
    For Function name, enter a name that describes the function, such as "StopEC2Instances".
    For Runtime, choose Python 3.9.
    Under Permissions, expand Change default execution role.
    Under Execution role, choose Use an existing role.
    Under Existing role, choose the IAM role.
    Choose Create function.
    On the Code tab, under Code source, paste the following code into the editor pane of the code editor on the lambda_function tab. This code stops the instances that you identify:
    Add the python code (EC2_stop.py)

    Test and Deploy the code for checking the EC2 stopping state.

# 4. Lambda EC2 Start Function

Open the Lambda console, 

    Choose Create function.
    Choose Author from scratch.
    Under Basic information, enter the following information:
    For Function name, enter a name that describes the function, such as "StopEC2Instances".
    For Runtime, choose Python 3.9.
    Under Permissions, expand Change default execution role.
    Under Execution role, choose Use an existing role.
    Under Existing role, choose the IAM role.
    Choose Create function.
    On the Code tab, under Code source, paste the following code into the editor pane of the code editor on the lambda_function tab. This code stops the instances that you identify:
    Add the python code (EC2_start.py)

    Test and Deploy the code for checking the EC2 stopping state.

# 5. Create the Rule for automatic run of Lambda Functions(Start and Stop)

    Go to Amazon EventBridge
    Go to Rules
    Define rule detail
    Give a name "Start-Stop_schedule"
    Click the Radio Control of "Schedule"
    Click on "Continue to Create Rule"
    Select the Schedule from Cron options
    Select the Target --> AWS Service --> Lambda Function --> Select the Stop_Lambda Function
    Create the schedule

# 6. Check the logs in CloudWatch

    Go to CloudWatch
    Go to Log groups
    Go to Stop_Ec2 logs
    Verify the logs as per schedule