from nt import environ
from aws_cdk import (
    Environment,
    Stack,
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_cloudwatch as cloudwatch
)
import aws_cdk
from constructs import Construct

class CdkpythonSsoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkpythonSsoQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
         # Create a new permission set with administrative access

        
  


        # Get the latest Amazon Linux 2023 AMI
        amazon_linux_2023_ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023,
           # edition=ec2.AmazonLinuxEdition.STANDARD,
            # virtualization=ec2.AmazonLinuxVirt.HVM,
           # storage=ec2.AmazonLinuxStorage.EBS
        )

        # Create a launch template


        launch_template = ec2.LaunchTemplate(
            self, "LaunchTemplate",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=amazon_linux_2023_ami,
            role=iam.Role(
                self, "InstanceRole",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
            )
        )

       

        # Define the mixed instances policy
        mixed_instances_policy = autoscaling.MixedInstancesPolicy(
            instances_distribution={
                "on_demand_base_capacity" : 1,  # One On-Demand instance as the base capacity
                "on_demand_percentage_above_base_capacity": 0,  # No additional On-Demand instances
                "spot_allocation_strategy": autoscaling.SpotAllocationStrategy.CAPACITY_OPTIMIZED,  # Use Spot instances for additional capacity
                "spot_max_price" : "0.05"
            },
            launch_template=launch_template
        )

        # Create the Auto Scaling group
        auto_scaling_group = autoscaling.AutoScalingGroup(      
            
            self, "MixedInstancesASG",
            vpc=ec2.Vpc.from_lookup(self, "VPC", is_default=True),
           # instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
           # machine_image=amazon_linux_2023_ami,
            min_capacity=1,
            max_capacity=2,
            desired_capacity=2,
            mixed_instances_policy=mixed_instances_policy
        )
         # Add a dynamic scaling policy based on CPU utilization


         
         # Add a dynamic scaling policy based on CPU utilization
       # Add a dynamic scaling policy based on CPU utilization
        step_scaling_policy = autoscaling.StepScalingPolicy(
            self, "StepScalingPolicy",
            auto_scaling_group=auto_scaling_group,
            metric=cloudwatch.Metric(
                namespace="AWS/EC2",
                metric_name="CPUUtilization",
                dimensions_map={"AutoScalingGroupName": auto_scaling_group.auto_scaling_group_name},
                statistic="Average",
                period=aws_cdk.Duration.minutes(1)

            ),
            scaling_steps=[

                autoscaling.ScalingInterval(
                    lower=0,
                    upper=20,
                    change=-1
                ),

                autoscaling.ScalingInterval(
                    lower=20,
                    upper=80,
                    change=0
                ),
                autoscaling.ScalingInterval(
                    lower=80,
                    upper=None,
                    change=1
                )
            ],
            adjustment_type=autoscaling.AdjustmentType.CHANGE_IN_CAPACITY

            
        )