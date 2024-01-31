# Automating the Developing and Deploying a Basic Web Application on Amazon EKS

This is a guide on how to Automating the Developing and Deploying a Basic Web Application on Amazon EKS <br>
using AWS CodePipeline. <br>
Whether you are new to Amazon EKS or looking to level up your skills, this repository has you covered.<br> Below are the steps to follow:

## Guide on How to Deploy a Basic Flask Web Application on Amazon EKS Using AWS CodePipeline

Below are the steps to follow:

## Table of Contents
- [Step 1: Create a Flask Web Application](#step-1-create-a-flask-web-application)
- [Step 2: Create a Dockerfile](#step-2-create-a-dockerfile)
- [Step 3: Create a requirements.txt File](#step-3-create-a-requirementstxt-file)
- [Step 4: Preparing Your Environment](#step-4-preparing-your-environment)
- [Step 5: Build and Push Docker Image to Amazon ECR](#step-5-build-and-push-docker-image-to-amazon-ecr)
- [Step 6: Step 6: Create Amazon ECR Pprivate Repository](#step-6-create-amazon-ecr-private-repository)
- [Step 7: Setup Amazon EKS Cluster Requirements](#step-7-setup-amazon-eks-cluster-requirements)
- [Step 8: Creating an Amazon EKS cluster](#step-8-creating-an-amazon-eks-cluster)
- [Step 9: Creating an Amazon EKS cluster](#step-9-creating-an-amazon-eks-cluster)
- [Step 10: Create a Kubernetes Deployment](#step-10-create-a-kubernetes-deployment)
- [Step 11: Set Up AWS CodePipeline](#step-10-set-up-aws-codepipeline)
- [Step 11: Test The Application](#step-11-test-the-application)


## Step 1: Create a Flask Web Application
Create a basic Flask web application. <br> [app.py](./app/app.py):

## Step 2: Create a Dockerfile
Create a Dockerfile to containerize the Flask application.<br> [Dockerfile](./Dockerfile):

## Step 3: Create a requirements.txt File
Create a `requirements.txt` file to list the Python dependencies.<br> [requirements.txt](./requirements.txt):

## Step 4: Preparing Your Environment
Assuming you have an Docker and Kubectl. if not <br> Below are the steps to follow:<br>
### 4.1. Update the installed packages and package cache on your instance.
    sudo apt-get update
    apt list --upgradable
    sudo apt upgrade -y

### 4.2. Installing Docker <br>
    sudo apt-get install docker.io -y

- Start the Docker service.

        sudo systemctl enable docker
        sudo systemctl start docker

- Add the `ubuntu user` to the `docker group` so you can execute Docker commands without using `sudo`.

        sudo usermod -aG docker ubuntu

- Log out and log back in again to pick up the new docker group permissions.

- Verify that the ubuntu can run Docker commands without sudo.

        docker run hello-world

- Troubleshoot Docker Engine installation.
- docker: permission denied while trying to connect to the Docker daemon socket<br>
        at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/create":<br>
        dial unix /var/run/docker.sock: connect: permission denied.

       sudo chmod 666 /var/run/docker.sock

       sudo addgroup docker

You can find the more guide [here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html).

`Note`: that Tutorial using `ubuntu-jammy-22.04-amd64-server` Operation System<br>
        Docker version `24.0.5`, build `24.0.5-0`ubuntu1`~22.04.1` <br>
For other Operation System Follow the Official Docker Documunts [here](https://docs.docker.com/desktop/).

### Step 5: Build and Push Docker Image to Amazon ECR.

Assuming you have an AWS account, follow these steps:

### 5.1. Set Up the AWS CLI
- AWS CLI install and update

        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install

before that step you may need to install `unzip` using `sudo apt install unzip`

- Confirm the installation

        aws --version

output: `aws-cli/2.15.13` Python/`3.11.6 `Linux/`6.2.0-1017`-aws exe/x86_64.ubuntu.22 `prompt/off`

- Configure the AWS CLI

        aws configure

AWS Access Key ID [None]:`<your AWS Access Key ID>`<br>
AWS Secret Access Key [None]:`<your-AWS Secret Access Key>` <br>
Default region name [None]:`<your-region>`<br>
Default output format [None]:

### 5.2. Build and Run Docker Image
- Open a terminal or command prompt and navigate to the directory containing the Dockerfile and run the following command:

        docker build -t my-eks-web-app .

- Run the newly built image

        docker run -p 5000:5000 my-eks-web-app

- Running Docker locally, point your browser to` http://localhost:5000/ `or `http://127.0.0.1:5000/`

### Step 6: Create Amazon ECR Private Repository.

* Create an ECR repository to store your Docker images.
* Make note of the repository URI
### 6.1. Ensure ECR Permissions

- Verify that your IAM user or role has the necessary permissions to access the ECR repository.<br>
 The required permissions include: <br>

`ecr:GetAuthorizationToken `<br>
`ecr:BatchCheckLayerAvailability` <br>

You can attach the `AmazonEC2ContainerRegistryPowerUs`er policy to your IAM user or role to grant these permissions.

### 6.2. Log in to AWS ECR

 ### *private Registry*

- Authenticate a private repository.

        aws ecr get-login-password --region `<your-region>` | docker login --username AWS --password-stdin `<aws_account_id>`.dkr.ecr.`<your-region>`.amazonaws.com

Replace `<your-region>` with your region.<br>
Replace `<aws_account_id>` with your aws_account_id <br>

### 6.3. Create a private repository

        aws ecr create-repository \
                --repository-name <repository-name> \
                --region <your-region>

Replace `<repository-name>` with your repository-name.<br>
Replace `<your-region>` with your region.<br>

### 6.4. Tag and Push Docker Image

- Tag the image to push to your private repository.<br>
- List the images you have stored locally to identify the image to tag and push.

        docker images

- Tag the image to push to `Amazon ECR private` repository.

        docker tag <image-name:tag> <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/<repository-name:tag>

- Push the image.

        docker push <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/<repository-name:tag>

Replace `<image-name:tag>` with your image-name:tag `ex: hello-world:latest`<br>
Replace `<aws_account_id>` with your aws_account_id.<br>
Replace `<your-region>` with your region.<br>
Replace `<repository-name>` with your repository-name.<br>
`Note`: ECR repository URI= `<aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/<repository-name:tag>`

Follow the Official Amazon Quick start: Publishing to `Amazon ECR Pprivate repository` using the AWS CLI [here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html).

  ### *Public Registry*

- Authenticate a public repository.

        aws ecr-public get-login-password --region <your-region> | docker login --username AWS --password-stdin public.ecr.aws

- Create a public repository
- Open a terminal or command prompt and navigate to the ECR directory and run the following command:.

        aws ecr-public create-repository \
             --repository-name <repository-name> \
             --catalog-data file://repositorycatalogdata.json \
             --region <your-region>

Replace `<repository-name>` with your repository-name.<br>
Replace `<your-region>` with your region.<br>

- Tag and Push an image to `Amazon ECR Public`repository. <br>
List the images you have stored locally to identify the image to tag and push.

        docker images

- Tag the image to push to your repository with your `public repository URI` <br>
which was in the response to the `create-repository` call you made in the previous step.

        docker tag <image-name:tag> public.ecr.aws/registry_alias/<repository-name>

- Push the image to the Amazon ECR

        docker push public.ecr.aws/registry_alias/<repository-name>

- Pull the image from the Amazon ECR

        docker pull public.ecr.aws/g7p1j8g3/hello-flask:v.1

Replace `<registry_alias>` with your registry_alias.<br>
Replace `<repository-name>` with your repository-name.<br>

Follow the Official Amazon Quick start: Publishing to `Amazon ECR Public` using the AWS CLI [here](https://docs.aws.amazon.com/AmazonECR/latest/public/getting-started-cli.html).

## Step 7: Set Up Amazon EKS Cluster
- Follow the official Amazon EKS Getting Started guide to create an Amazon EKS cluster.
- Download the kubectl binary for your cluster's Kubernetes version from Amazon S3.
- Kubernetes 1.29

        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.29.0/2024-01-04/bin/linux/amd64/kubectl

- Apply execute permissions to the binary.

        chmod +x ./kubectl

- Copy the binary to a folder in your PATH.

        mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH

-Verify EKS Version.

        kubectl version --client

## Step 7: Setup Amazon EKS Cluster Requirements.

### 7.1. Create an Amazon IAM Policy Role.

- Create IAM Policy Role
- Create a cluster IAM role and attach the required Amazon EKS IAM managed policy to it.
- Open a terminal or command prompt and navigate to the `EKS directory` and run the following command:.

        aws iam create-role   --role-name <Policy-Role-Name>  --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"

- Attach Policy Role
- Attach the required Amazon EKS managed IAM policy to the role.
-
        aws iam attach-role-policy   --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy   --role-name EKS-Cluster-trust-policy-role

### 7.2. Create an Amazon VPC
- Create an Amazon VPC with public and private subnets that meets Amazon EKS requirements
- Open a terminal or command prompt and navigate to the `cloudformation directory` and run the following command:.

        aws cloudformation create-stack --region <your-region> --stack-name <stack-name> --template-body file://amazon-eks-vpc-private-subnets.yaml

- Navigate to the `cloud-formation outputs` and write down:<br>
            - Subnets IDs in the **VPC** `<PrivateSubnet01>, <PrivateSubnet02>, <PublicSubnet01>, <PublicSubnet02>`<br>
            - **SecurityGroups** `<Security group>`

## Step 8: Creating an Amazon EKS cluster.

### 8.1.Create-cluster

        aws eks create-cluster --region <your-region> --name <cluster-name> --kubernetes-version 1.29 \
           --role-arn arn:aws:iam::<aws_account_id>:role/myAmazonEKSClusterRole \
           --resources-vpc-config subnetIds=<PrivateSubnet01>,<PrivateSubnet02>,<PublicSubnet01>,<PublicSubnet02>,securityGroupIds=<Security-group>

Replace `<your-region>` with your **region**.<br>
Replace `<cluster-name>` with your **cluster name**. <br>
Replace `<aws_account_id>` with your **aws_account_id**.<br>
Replace `<PrivateSubnet01>,<PrivateSubnet02>,<PublicSubnet01>,<PublicSubnet02>` with your **public** and **private** subnets from `cloud-formation outputs`.<br>
Replace `<Security-group>` with your **Security group**

 ### 8.2. Configure your computer to communicate with your cluster

        aws eks update-kubeconfig --region <your-region> --name <cluster-name>

 ### 8.3. Confirm communication with your cluster by running the following command.

        kubectl get svc

## Step 9: Create a Node Group

### 9.1 Create a Node AIM Policy Role

- Create a node IAM role and attach the required Amazon Node IAM managed policy to it.
- Open a terminal or command prompt and navigate to the `EKS directory` and run the following command:.

        aws iam create-role \
          --role-name AmazonEKSNodeRole \
          --assume-role-policy-document file://"node-role-trust-relationship.json"

- Attach Policy Role.
- Attach the required `Amazon EKS Worker Node` `Amazon and EC2 Container Registry ReadOnly` Policy to the role.

        aws iam attach-role-policy \
          --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
          --role-name AmazonEKSNodeRole

        aws iam attach-role-policy \
          --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
          --role-name AmazonEKSNodeRole

- Determine the IP family of your cluster.

        aws eks describe-cluster --name my-cluster | grep ipFamily

depending on which IP family you created your cluster with.

        aws iam attach-role-policy \
          --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
          --role-name AmazonEKSNodeRole

 Follow the Official `Amazon EKS node IAM role` using the AWS CLI [here](https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html)

### 9.2 Create a Node Group

        aws eks create-nodegroup \
            --cluster-name <cluster-name> \
            --nodegroup-name <nodegroup-name> \
            --scaling-config min-size=2,max-size=3 \
            --subnets <Subnet01>,<Subnet02> \
            --instance-types t3.small \
            --disk-size 8 \
            --ami-type AL2_x86_64 \
            --node-role-arn arn:aws:iam::<aws_account_id>:role/<nodegroup-role>

Replace `<cluster-name>` with your **cluster name**. <br>
Replace `<nodegroup-name>` with your **nodegroup-name**.<br>
Replace `<aws_account_id>` with your **aws_account_id**.<br>
Replace `<nodegroup-role>` with your **AmazonEKSNodeRole** AIM Role from .


## Step 10: Create a Kubernetes Deployment.

 ### 10.1. Create a Kubernetes deployment file.<br> [deployment.yaml](./deployment.yaml):<br>

Replace `<your-ecr-repository-uri>` with your ECR repository URI.

 ### 10.2. Apply the Deployment
- Apply the Kubernetes Deployment:

         kubectl apply -f deployment.yaml



## Step 11: Test the Application

Wait for the LoadBalancer service to be assigned an external IP address:


- Obtain the Load Balancer URL:

       kubectl get svc my-eks-web-app -w

Once the external IP is available, you can access your web application in a browser using that IP.

#####################################################################################################################
#                                                                                                                    #
  Keep in mind that this example is minimal and focuses on the basic steps. <br>
  In a production scenario, you would likely include more `features`, `security measures`, and `configurations`.<br>
  Additionally, you might want to explore tools like `Helm` for managing `Kubernetes manifests` more efficiently.
#                                                                                                                    #
######################################################################################################################

## Step 10: Set Up AWS CodePipeline
Follow these steps to set up AWS CodePipeline:

### 10.1. Create an S3 Bucket for CodePipeline Artifacts

    aws s3api create-bucket --bucket <bucket- name> --region <your-region>

### 10.2. Create a CodePipeline IAM Role
Create an **IAM role** with the **necessary permissions** for CodePipeline.<br>
Attach the  policies.<br>
`AmazonEKSClusterPolicy`, <br>
`AWSCodePipelineCustomEKSContainerPolicy`

 1. Create an IAM role:

            aws iam create-role --role-name CodePipelineEKSRole --assume-role-policy-document file://trust-policy.json

2. Attach the following policies to the role:

   ```
   aws iam attach-role-policy --role-name CodePipelineEKSRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
   ```

   ```
   aws iam attach-role-policy --role-name CodePipelineEKSRole --policy-arn arn:aws:iam::aws:policy/AWSCodePipelineCustomEKSContainerPolicy
   ```

3. Grant the role access to the Amazon EKS cluster:

           aws eks update-cluster-config --name eks-cluster-name --role-arn arn:aws:iam::account-id:role/CodePipelineEKSRole


4. **Configure CodePipeline to use the role:**

   In the CodePipeline console, create a new pipeline or edit an existing one.

   Under **Service role**, select the `CodePipelineEKSRole` role.



### 10.3. Create CodePipeline
Use the AWS Management Console or AWS CLI to create a CodePipeline. <br>
Set up the source (GitHub or other) and configure the build stage using CodeBuild.<br>
- Follow these step
1. Open the **AWS Management Console**.
2. Navigate to the **CodePipeline service**.
3. Click on **Create pipeline**.
4. Provide a name for your pipeline (e.g., my-eks-web-app-pipeline).
5. choose the Pipeline type **v.2** or **v.1**
6. In the Service role section, choose the **IAM role** you created in the previous step.<br>
7. `Artifact store:` **S3 Bucket** you created in the previous step
Click on **Next** .

#### 10.3.1 Add Source Stage
- Follow these step
1. Choose the source provider for your code (e.g., GitHub).
2. Connect to your GitHub repository and configure the branch choose **main**.
3. Choose a repository that you have already created where you have pushed your source code.
4. Choose a branch of the repository Branch name **main**
5. Choose a detection mode to automatically start your pipeline when a change occurs in the source code. **AWS CodePipeline**
6. Choose the output artifact format uses the default **zip format**.<br>
Click on Next.

#### 10.3.2 Add Build Stage (CodeBuild)
- Follow these step
For the `build provider`: **AWS CodeBuild**.<br>
If you don't have an existing **CodeBuild** project, create a new one. Provide a name and configure the build settings:<br>
- Follow these step to Create build project:
1. Choose a `Project name`
2. `Environment Image:` **Custom image**.
3. `Environment Type:` **Linux EC2**
4. `Image registry:` **ECR** or **Docker registry**
5. `ECR account:` **My ECR account**
6. `ECR repository:` **Repository-name**
7. `ECR image:` **image name**
8. `Image pull credentials:`
9. `Role:` Existing service role (choose the **CodeBuild** role you created earlier)
10. `Buildspec:` Use a buildspec file **buildspec.yml** . <br>
Click on **Continue to CodePipeline**.
11. `Build type:` **Single build**

#### 10.3.3 Add Deploy Stage (Amazon EKS)
- Follow these step
For the deploy provider, choose Amazon EKS.<br>
Configure the deployment settings:<br>
1. `Cluster Name:` Choose the **EKS cluster** you created earlier.<br>
2. `Region:` Choose your **AWS region**.<br>
3. `Namespace:` Provide a **Kubernetes namespace** for your application (e.g., default).<br>
4. `Service Name:` Provide the name of the **Kubernetes service** you defined in the **deployment.yaml**.<br>
Click on Next.<br>

#### 10.3.4 Review and Create
Review the pipeline configuration.<br>
Click on **Create pipeline**.<br>

Your CodePipeline is now set up, and it will automatically trigger when changes are pushed to the source repository. <br>
The pipeline will build the Docker image, push it to ECR, and deploy the updated application to your **Amazon EKS cluster**.

## Step 11: Test the Application
Once the CodePipeline completes, check the progress in the **AWS CodePipeline console**.<br>
you should be able to access your web application.

- Obtain the Load Balancer URL:

        kubectl get svc my-eks-web-app -w

Access the application using the **Load Balancer URL**.

Congratulations! You've successfully set up a **CI/CD pipeline** for a containerized web application on **Amazon EKS**.

Amazon Elastic Container Service:

Cluster name

Default namespace
Infrastructure
Amazon EC2 instances
Manual configurations
Auto Scaling group
Provisioning model On-demand Spot
Operating system/Architecture Linux2
EC2 instance type t2 micro

aws deploy create-deployment-group \
    --application-name my-eks-web-app \
    --deployment-group-name my-eks-web-app-deploy-gr \
    --deployment-config-name CodeDeployDefault.ECSAllAtOnce \
    --service-role-arn arn:aws:iam::307169715738:role/CodeDeploy-Access-EC2-Auto-Scaling\
    --ecs-services my-eks-web-app-ecs-ser\
    --target-group-info-list targetGroupInfoList=[{name=target1},{name=target2}] \
    --load-balancer-info elbInfoList=[{name=my-eks-web-app-load-balancer}]

aws deploy create-deployment-group \
    --application-name my-app \
    --deployment-group-name my-deployment-group \
    --deployment-config-name CodeDeployDefault.ECSAllAtOnce \
    --service-role-arn arn:aws:iam::123456789012:role/CodeDeployServiceRole \
    --ecs-services ecs-service-name \
    --target-group-info-list targetGroupInfoList=[{name=targetGroup1},{name=targetGroup2}] \
    --load-balancer-info elbInfoList=[{name=my-load-balancer}]
