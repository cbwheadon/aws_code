import boto
from boto.ec2.autoscale import AutoScaleConnection
import boto.ec2.autoscale
import boto.ec2.cloudwatch
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy
from boto.ec2.cloudwatch import MetricAlarm
import sys

ami = sys.argv[1]

conn = boto.connect_autoscale()
#Create launch configuration
lc = LaunchConfiguration(name='my-launch_config', image_id=ami, instance_type='t1.micro',key_name='ebs',security_groups=['autoscale'], spot_price=0.006)
conn.create_launch_configuration(lc)

#Create auto-scaling group
ag = AutoScalingGroup(group_name='my_group', load_balancers=['NMMBalancer'],availability_zones=['eu-west-1b'],launch_config=lc, min_size=1, max_size=8,connection=conn)
conn.create_auto_scaling_group(ag)

#Policies
scale_up_policy = ScalingPolicy(name='scale_up', adjustment_type='ChangeInCapacity',as_name='my_group', scaling_adjustment=1, cooldown=180)
scale_down_policy = ScalingPolicy(name='scale_down', adjustment_type='ChangeInCapacity',as_name='my_group', scaling_adjustment=-1, cooldown=180)

conn.create_scaling_policy(scale_up_policy)
conn.create_scaling_policy(scale_down_policy)

#Refresh policy information
scale_up_policy = conn.get_all_policies(as_group='my_group', policy_names=['scale_up'])[0]
scale_down_policy = conn.get_all_policies(as_group='my_group', policy_names=['scale_down'])[0]

#Set up alarm
cloudwatch= boto.ec2.cloudwatch.connect_to_region('eu-west-1')
alarm_dimensions = {"AutoScalingGroupName": 'my_group'}

scale_up_alarm = MetricAlarm(name='scale_up_on_cpu', namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='>', threshold='70',period='60', evaluation_periods=2,alarm_actions=[scale_up_policy.policy_arn],dimensions=alarm_dimensions)

scale_down_alarm = MetricAlarm(name='scale_down_on_cpu', namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='<', threshold='40',period='60', evaluation_periods=2,alarm_actions=[scale_down_policy.policy_arn],dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_down_alarm)
cloudwatch.create_alarm(scale_up_alarm)
