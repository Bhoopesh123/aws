# EKS Cluster Creation on AWS Cloud  

Kindly follow the below steps to create EKS Kubernetes Cluster on AWS Cloud

# 1. Go to the below link for creating a new Cluster  

    https://ap-south-1.console.aws.amazon.com/eks/home?region=ap-south-1#/clusters


# 2. Create Cluster Role as below: 

    Give name as "eks-first-cluster"
    Create Service Role
    https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html#create-service-role
        1. Open the IAM console at https://console.aws.amazon.com/iam/.
        2. Choose Roles, then Create role.
        3. Under Trusted entity type, select AWS service.
        4. From the Use cases for other AWS services dropdown list, choose "EKS".
        5. Choose "EKS - Cluster" for your use case, and then choose Next.
        6. On the Add permissions tab, choose Next.
        7. For Role name, enter a unique name for your role, such as "eksClusterRole".
        8. For Description, enter descriptive text such as "My First EKS Cluster Role".
        9. Choose Create role.

# 3. Cluster Creation Process  

    1. Choose default configurations under "Specify Networking" section then click Next
    2. Don't enable any logging to save cost then click Next
    3. Select default addons then click next
    4. Review and Create and click next.

# 4. Add node group to your cluster  

1. Mention the Node Configuration  
2. Create a node IAM Role  
    https://us-east-1.console.aws.amazon.com/iamv2/home#/roles  
3. To create your Amazon EKS node role in the IAM console  
    a. Open the IAM console at https://console.aws.amazon.com/iam/.  
    b. In the left navigation pane, choose Roles.  
    c. On the Roles page, choose Create role.  
    d. On the Select trusted entity page, do the following:  
    e. In the Trusted entity type section, choose AWS service.  
    f. Under Use case, choose EC2.  
    g. Choose Next.  
    h. On the Add permissions page, do the following:  
    i. In the Filter policies box, enter AmazonEKSWorkerNodePolicy.  
    j. Select the check box to the left of AmazonEKSWorkerNodePolicy in the search results.  
    k. Choose Clear filters.  
    l. In the Filter policies box, enter AmazonEC2ContainerRegistryReadOnly.  
    m. Select the check box to the left of AmazonEC2ContainerRegistryReadOnly in the search results.  
    n. Either the AmazonEKS_CNI_Policy managed policy, or an IPv6 policy that you create must also be attached to either this role or to a different role that's mapped to the aws-node Kubernetes service account. We recommend assigning the policy to the role associated to the Kubernetes service account instead of assigning it to this role. For more information, see Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts.  
    o. Choose Next.  
    p. On the Name, review, and create page, do the following:  
    q. For Role name, enter a unique name for your role, such as AmazonEKSNodeRole.  
    r. For Description, replace the current text with descriptive text such as Amazon EKS - Node role.  
    s. Under Add tags (Optional), add metadata to the role by attaching tags as key–value pairs. For more information about using tags in IAM, see Tagging IAM Entities in the t. IAM User Guide.  
    u. Choose Create role.  

4. Select the node group role that has been created in above section.

# 5. Connect to Cluster  

    If aws cli is not installed use the below commands to install it  

    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"  
    unzip awscliv2.zip  
    sudo ./aws/install  

    aws configure  
    aws sts get-caller-identity  
    aws eks --region ap-south-1 update-kubeconfig --name eks-first-cluster  
    kubectl run mycurlpod --image=curlimages/curl -i --tty -- sh  
