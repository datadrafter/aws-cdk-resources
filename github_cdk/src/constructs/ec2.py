from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancing as elb,
    core,
)

class CdkSimpleUbuntuInstanceAsg(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #############################################
        ### Setup a basic vpc and security groups ###
        #############################################

        # Create a simple vpc
        vpc = ec2.Vpc(self, "MyVPC",
          max_azs=3
        )

        # My existing ssh key pair name
        keypair='harry'

        # Dynamically pull ubuntu ami id - needs environment var set CDK_DEFAULT_REGION
        dynamic_ubuntu_ami = ec2.MachineImage.lookup(
            name="*ubuntu-bionic-18.04-amd64-server*",
            owners=["099720109477"]
        )

        # Security group for our test instance
        my_sg = ec2.SecurityGroup(
            self,
            "my_sg",
            vpc = vpc,
            description="My sg for testing",
            allow_all_outbound = True
        )
        # Add ssh from anywhere
        my_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(22),
            "Allow ssh access from anywhere"
        )

        #################################################################
        # Single Ubuntu EC2 instance in Private Subnet in an ASG of 1:1 #
        #################################################################
        asg = autoscaling.AutoScalingGroup(
            self,
            "Ubuntu-ASG-Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=dynamic_ubuntu_ami,
            key_name=keypair,
        )
        asg.add_security_group(my_sg) # add our security group, expects object

        ########################################################
        # Single Ubuntu EC2 instance in Private Subnet, no ASG #
        ########################################################
        ubuntu_ami=dynamic_ubuntu_ami.get_image(self).image_id # CfnInstances requires image_id to be the ami string
        instance = ec2.CfnInstance(
            self,
            "Ubuntu-Instance",
            image_id=ubuntu_ami,
            instance_type='m4.large',
            monitoring=True,
            key_name=keypair,
            network_interfaces = [{
                "deviceIndex": "0",
                "associatePublicIpAddress": False,
                "subnetId": vpc.private_subnets[0].subnet_id,
                "groupSet": [my_sg.security_group_id]
            }],
        )

        ###################################################
        # Bastion host to access Ubuntu hosts for testing #
        ###################################################
        host = ec2.BastionHostLinux(self, "BastionHost",
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )
        host.allow_ssh_access_from(ec2.Peer.ipv4("0.0.0.0/0")) # Restrict this to your IP
        host.instance.instance.add_property_override("KeyName", keypair) # Add keypair for access unless you use SSM

class NLBStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")

        # Security group for our test instance
        my_sg = ec2.SecurityGroup(
            self,
            "my_sg",
            vpc = vpc,
            description="My sg for testing",
            allow_all_outbound = True
        )
        # Add ssh from anywhere
        my_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow ssh access from anywhere"
        )

        asg = autoscaling.AutoScalingGroup(
            self, "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(),
        )
        asg.add_security_group(my_sg) # add our security group, expects object

        ## Classic Elastic Load Balancer
        #lb = elb.LoadBalancer(
        #    self, "ELB",
        #    vpc=vpc,
        #    internet_facing=True,
        #    health_check={"port": 22}
        #)
        #lb.add_target(asg)
        #
        #listener = lb.add_listener(
        #    external_port=8000,
        #    external_protocol=elb.LoadBalancingProtocol.TCP,
        #    internal_port=22,
        #    internal_protocol=elb.LoadBalancingProtocol.TCP
        #)
        #listener.connections.allow_default_port_from_any_ipv4("Open to the world")

        # Network Load Balancer
        nlb = elbv2.NetworkLoadBalancer(
            self, "NLB",
            vpc=vpc,
            internet_facing=True,
            cross_zone_enabled=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )

        my_target = elbv2.NetworkTargetGroup(
            self, "MyTargetGroup",
            port=22,
            vpc=vpc
        )

        listener = nlb.add_listener(
            "Listener",
            port=8000,
            default_target_groups=[my_target]
        )
        my_target.add_target(asg)