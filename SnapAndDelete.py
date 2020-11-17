import boto3
import botocore

GAMING_INSTANCE_NAME = 'YOUR GAMING RIG NAME GOES HERE'
GAMING_INSTANCE_REGION = 'eu-west-3'
GAMING_INSTANCE_SIZE_GB = 512


def lambda_handler(object, context):
    ec2 = boto3.client('ec2')

    # Connect to region
    ec2 = boto3.client('ec2',region_name=GAMING_INSTANCE_REGION)
    res_client = boto3.resource('ec2', region_name=GAMING_INSTANCE_REGION)

    # Get all available volumes    
    volumes = ec2.describe_volumes( Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes'] 
    
    # Get all volumes for the given instance    
    volumes_to_delete = []
    for volume in volumes:
        for tag in volume['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] == GAMING_INSTANCE_NAME:
                volumes_to_delete.append(volume)
                
    if len(volumes_to_delete) == 0:
        print('No volumes found. Nothing to do! Aborting...')
        return
                
    # Create a snapshot of the volumes
    snaps_created = []
    for volume in volumes:
        snap = ec2.create_snapshot(VolumeId=volume['VolumeId'])
        snap_id = snap['SnapshotId']
        snap_waiter = ec2.get_waiter('snapshot_completed')
        
        try:
            snap_waiter.wait(SnapshotIds=[snap_id], WaiterConfig={'Delay': 15,'MaxAttempts': 59 })
        except botocore.exceptions.WaiterError as e:
            print("Could not create snapshot, aborting")
            print(e.message)
            return
            
        print("Created snapshot: {}".format(snap['SnapshotId']))
        snaps_created.append(snap['SnapshotId'])
        
    # Tag the snapshots
    if len(snaps_created) > 0:
        ec2.create_tags(
            Resources=snaps_created,
            Tags=[
                {'Key': 'SnapAndDelete', 'Value': 'True'},
                {'Key': 'Name', 'Value': "Snapshot of " + GAMING_INSTANCE_NAME}
            ]
        )
    
    # Delete any current AMIs
    images = ec2.describe_images(Owners=['self'])['Images']
    for ami in images:
        if ami['Name'] == GAMING_INSTANCE_NAME:
            print('Deleting image {}'.format(ami['ImageId']))
            ec2.deregister_image(DryRun=False,ImageId=ami['ImageId'])
    
    # Remove previous snapshots of the volumes
    previous_snapshots = ec2.describe_snapshots(Filters=[{'Name': 'tag-key', 'Values': ['SnapAndDelete']}])['Snapshots']
    for snapshot in previous_snapshots:
        if snapshot['SnapshotId'] not in snaps_created:
            print("Removing previous snapshot: {}".format(snapshot['SnapshotId']))
            ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
    
    # Delete the volumes
    for volume in volumes_to_delete:
        v = res_client.Volume(volume['VolumeId'])
        print("Deleting EBS volume: {}, Size: {} GiB".format(v.id, v.size))
        v.delete()

    # Create a new AMI
    if len(snaps_created) > 0:
        amis_created = []
        ami = ec2.register_image(
            Name=GAMING_INSTANCE_NAME, 
            Description=GAMING_INSTANCE_NAME + ' Automatic AMI', 
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'DeleteOnTermination': False,
                        'SnapshotId': snaps_created[0],
                        'VolumeSize': GAMING_INSTANCE_SIZE_GB,
                        'VolumeType': 'gp2'
                    }
                },
            ],
            Architecture='x86_64', 
            RootDeviceName='/dev/sda1', 
            DryRun=False, 
            VirtualizationType='hvm', 
            EnaSupport=True #Supported instance types: current generation instance type, other than C4, D2, M4 instances smaller than m4.16xlarge, or T2. https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/enhanced-networking-ena.html
            #SriovNetSupport='simple' Supported instance types: C3, C4, D2, I2, M4 (excluding m4.16xlarge), and R3. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sriov-networking.html
        )
        print('Created image {}'.format(ami['ImageId']))
        amis_created.append(ami['ImageId'])
        
        if len(amis_created) > 0:
            # Tag the AMI
            ec2.create_tags(
                Resources=amis_created,
                Tags=[
                    {'Key': 'SnapAndDelete', 'Value': 'True'},
                    {'Key': 'Name', 'Value': GAMING_INSTANCE_NAME}
                ]
            )
