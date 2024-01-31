aws elbv2 create-load-balancer \
    --name my-load-balancer \
    --type application \
    --subnets subnet-01234567,subnet-76543210

aws elbv2 create-target-group \
    --name my-target-group \
    --protocol HTTP \
    --port 80 \
    --target-type instance \
    --vpc-id vpc-12345678
```

2. **Create an ECS Service**:

```
aws ecs create-service \
    --cluster my-cluster \
    --service-name my-service \
    --task-definition my-task-definition \
    --desired-count 1 \
    --load-balancers \
        targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-target-group
```

3. **Create an ECS Deployment Group**:

```
aws deploy create-deployment-group \
    --application-name my-application \
    --deployment-group-name my-deployment-group \
    --service-role-arn arn:aws:iam::123456789012:role/ecsServiceRole \
    --deployment-config-name CodeDeployDefault.OneAtATime \
    --auto-scaling-groups \
        my-asg-1,my-asg-2
```

4. **Configure Deployment Group to Use Load Balancer**:

```
aws deploy update-deployment-group \
    --application-name my-application \
    --deployment-group-name my-deployment-group \
    --load-balancer-info ELB=my-load-balancer,TargetGroupPair={TargetGroup=my-target-group,ProdTrafficRoute=TrafficRoute}
```


5. **Trigger a Deployment**:

```
aws deploy create-deployment \
    --application-name my-application \
    --deployment-group-name my-deployment-group \
    --revision S3://my-bucket/my-deployment-package/1
```

6. **Monitor Deployment**:

```
aws deploy get-deployment \
    --application-name my-application \
    --deployment-group-name my-deployment-group \
    --deployment-id 1
