import boto
import time

conn = boto.connect_autoscale()
ags = conn.get_all_groups()
ags[0].shutdown_instances()
time.sleep(60)
ags[0].delete()
time.sleep(5)
lcs = conn.get_all_launch_configurations()
lcs[0].delete()
