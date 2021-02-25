Parsec AWS Automation Scripts & Guide
=====================================

| Info        | Value           |
| ------------- |:-------------|
| Created by      | Keith Vassallo |
| Acknowledgements      | [/u/rom-ok](https://www.reddit.com/user/rom-ok)<br>[/u/dolanders](https://www.reddit.com/user/dolanders)<br>[@Cookie-Monster-Coder](https://github.com/Cookie-Monster-Coder)<br>[@rhigueras](https://github.com/rhigueras)<br>[@srichter](https://github.com/srichter)<br>The [Parsec Team](https://parsecgaming.com/)      |
| Related Reading      | [Parsec AWS Guide](https://blog.parsecgaming.com/rtx-cloud-gaming-with-the-new-aws-g4-instances-11d1c60c2d09) |

Check out a video version of this guide at: https://www.youtube.com/watch?v=gE20QLY6gAI

## Table of Contents

**[Aims](#aims)**<br>
**[Setting up the Server](#setting-up-the-server)**<br>
**[Installing Parsec](#installing-parsec)**<br>
**[Creating the Automation Script](#creating-the-automation-script)**<br>
**[Creating the Start Script](#creating-the-start-script)**<br>
**[Putting it All Together](#putting-it-all-together)**<br>

## Aims

The aims of this guide are as follows:

* Roll your own cloud gaming server.
* Be able to install any game you want, regardless of which store it's available on, and even if it's not in any store.
* Do it as cheaply as possible.
* Automate it such that when you're done gaming, you just need to shutdown the server.

## Setting up the Server

We'll begin by following the Parsec AWS guide. 

1. If you haven't already, create a [Parsec Account](https://parsecgaming.com/signup/) and download the [Parsec Client](https://parsecgaming.com/downloads)
2. If you haven't already, create an [AWS Account]().
3. Optionally, create a [Razer Account](https://aws.amazon.com/registration-confirmation/).
4. Download Microsoft Remote Desktop Client [for Windows](https://www.microsoft.com/en-us/p/microsoft-remote-desktop/9wzdncrfj3ps?activetab=pivot:overviewtab) or [for macOS](https://docs.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-mac) or something like [Remmina](https://flathub.org/apps/details/org.remmina.Remmina) for Linux.
4. Login to the [AWS Console](https://console.aws.amazon.com) using your root account.
5. Go to **Services > EC2**.
6. Click on **Running Instances**.

![Running instances](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/running_instances.png)

7. Choose a region closest to you (from the top right). 

![Region selection](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/region.png)

8. Click **Launch Instance**. Select **Windows Server 2019 Base**. 

![2016 Base](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/2019Base.png)

9. From the next screen, choose the **g4dn.xlarge** instance type. 

![g4dn.xlarge instance](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/g4dnxlarge.png)

10. Click **Next: Configure Instance Details**.

11. Leave all options unchanged, and move on to **Next: Add Storage**. From here, you will need to choose how big you want your disk to be. I chose 512GB, since it's roomy and I typically don't leave all my games installed at once. Of course, you can choose any size you want here, but bear in mind you are charged per GB. Choose **General Purpose SSD (gp2)** as the storage type and make sure you turn **OFF** the **Delete on Termination** checkbox. This ensures our volume isn't destroyed when we shutdown our machine. We'll be creating a script to handle that part for us. 

![Adding storage](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/storage.png)

12. Move on to **Next: Add Tags**. This is **Very Important** so don't skip it. You'll want to create a tag called **Name** - with a capital **N**. For the value, choose a name for your gaming server. Make sure that the checkboxes for both **Instances** and **Volumes** are checked.

![Tagging the instance](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tagginginstance.png)

13. Move on to **Next: Configure Security Group**. Leave the default option to create a new security group, and give it an easy-to-remember name, such as **Your_Instance_Name_Here-Sg**.

![Create security group](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/SecurityGroup.png)

14. Now click **Review and Launch** and click **Launch**. You'll be asked to create a key pair. Click **Create a new key pair** and give the key a name. 

![Create a key pair](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/createkeys.png)

15. **Download** the key and keep it somewhere safe. I strongly recommend you create a folder on your system to keep all documents related to your gaming rig. From now on, I'll refer to this as **That Folder**.

16. Finally, click **Launch Instances**. Now, you'll get a message that your instance was launched successfully.

17. Our instance has launched! To confirm, click **View Instances** and then click **Instances**. You'll see the instance is starting or has already started. 

![Instance started](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/instance_started.png)

18. Now we'll connect to the instance. With your instance selected, click **Connect**, then switch to the **RDP client** tab, click **Download Remote Desktop File** and add it to **That Folder**. Next, click **Get Password**. If you get a warning about the password not being available yet, close the window and clikc **Connect** again after a few minutes. Browse to the location of your key file (it should be in **That Folder**). This will display the key contents in the window.

![Decrypted password](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/decrypted.png)

29. Click **Decrypt Password**. You will be shown the username (**Administrator**) and your password. Save these somewhere safe, I suggest in **That Folder** at first, but eventually move these to a proper password manager.

## Installing Parsec

We'll now install Parsec via their awesome script, which will also install other stuff to make our life easier, as well as update the GPU drivers.

1. Double-click on the RDP file you downloaded earlier, this will open a connection in Microsoft RDP Client, with the username already filled in. Simply paste the password and click **Connect**. You will connect to the desktop of the instance.

2. Now click **Start** and type **PowerShell**, click on **Windows PowerShell**. Now we need to get the Parsec setup script. Head on over to the [Parsec Cloud Preparation Tool GitHub](https://github.com/jamesstringerparsec/Parsec-Cloud-Preparation-Tool) and copy the script given:

![Parsec cloud prep tool](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/prepcopy.png)

3. Now, back in your RDP session, paste the script in PowerShell. This will extract a compress file. Press **Enter** to continue the process.

![Parsec cloud prep tool 1](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps1.png)

4. You will be asked whether to configure automatic Windows login. Type **Y** to accept this. You will be asked for your username and password, which you placed earlier in **That Folder**. 

![Parsec cloud prep tool 2](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps2.png)

5. The script will now install a bunch of stuff, including DirectX 11, Chrome, Parsec and 7zip. Depending on the script version, AWS, Microsoft and the alignment of the moon, you may sometimes get errors from the script. These will probably show that one or more downloads failed, typically for Direct X and the XBox Game controller driver. If you do get this error, you can download Direct X from [here](https://community.pcgamingwiki.com/files/file/2106-legacy-directx-sdk-redist-directx_jun2010_redistexe/) and the XBox contoller driver from [here](https://www.techspot.com/drivers/driver/file/information/11300/).

![Script errors](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/pserror.png)

6. When Parsec is installed, you'll see the Parsec client - go ahead and login. The login won't work at first, but you'll receive an e-mail asking you to confirm your location. Click on **Approve your new location** once you get the email, then login to Parsec on your gaming server.

7. Eventually you'll see a pop-up for Razer Synapse - asking you to login. You don't need to login - we just need this installed. Go ahead and close it. **Note: On Windows Server 2016 you may need to login and/or close the app for the script to continue.**. 

![Parsec cloud prep tool 3](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps3.png)

8. The Parsec script will now continue with the GPU updater tool. You'll be prompted to provide an Access Key and Secret. To do this, copy the link that is shown in the prompt, and paste it in your browser, or just [click here](https://console.aws.amazon.com/iam/home?/security_credentials#/security_credentials). 

![Parsec cloud prep tool 5](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps5.png)

9. Now click on **Access keys (access ID and secret access key)** and click **Create New Access Key**. Click **Download Key File** and add this to **That Folder**. Then click **Show Access Key** - this will show the access key and secret access key. Copy the first one and paste it in the PowerShell window, pressing **Enter**. Then copy the secret key and also paste it in PowerShell, followed by **Enter**. You'll be asked whether to save the access key - type **y**. Answer the next two questions with **y**.

![Parsec cloud prep tool 6](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps6.png)

10. When the driver is installed, you'll be advised whether or not you need to reboot.

11. If you rebooted, use the steps outlined in step 1 to re-connect to your system via RDP.

12. At this point you should configure Parsec (double-click the Parsec icon on your desktop). I used the following settings:

- Host Settings
  - If you're on macOS, change **Resolution** to match the resolution of your personal system. You can find this out by clicking **Apple > About this Mac > Displays**. If you don't do this, connecting via Parsec will fail to change the resolution of the server to match your system. Windows/Linux users don't need to do this.
  - Increase the **Bandwidth Limit** to **50 Mbps**.
  - Give the host an easy to remember name.
- Client Settings - not really required, but ¯\_(ツ)_/¯
  - Change **Resolution** to match your setting from above.
  - Set **H.265 (HEVC)** to **On**.
  
13. At this point, the Parsec client on your system should show the server as available.

![Parsec server found](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/serverok.png)

14. Optionally, double-click on the **Setup Auto Shutdown** icon on your desktop. This will shutdown your system after a number of minutes if its idle, just in case you forget to do it yourself. When prompted, I set it to 45 minutes. 

15. Optionally, doublick-click on the **Setup One Hour Warning** icon on your desktop. This will warn you when you have been connected for an hour, so you can better manage your billing.

16. Now, disconnect from your server (i.e. close the RDP window), and connect to the server via Parsec instead. You're now ready to game! If you're not interested in the automation stuff, you can now skip to the [Gaming](#gaming) section. 

## Creating the Automation Script

This section is optional - however it might be something you look into. This basically configures the following:

- When you're done gaming, you just shutdown the server.
- The script is called automatically when the server is terminated. It:
  - Takes a snapshot of the volume.
  - Creates an AMI of from the snapshot.
  - Deletes the volume
  - Deletes old snapshots and AMIs.
  
The reason we do this is because keeping a snapshot is cheaper than keeping a volume. We also have an AMI so we can easily re-launch the instance later and continue where we left off. I've also created a script to do this automatically, which is described in the next section.

1. Shutdown your rig (**Start > Shutdown**) then from the AWS console, go to **Services > Lambda**. 

2. Click **Create Function** and give it a name. In my case I called it **SnapAndDelete** - but any name will do. For the **Runtime**, choose **Python 3.8**. Then click **Create Function**.

![Create Lambda function](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/createfunction.png)

3. You'll see a code editor where you can create your function. Grab the function code from [here](https://github.com/keithvassallomt/parsec-aws-automation/blob/master/SnapAndDelete.py), and paste it in the code editor. 

![Pasted function](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/pastedfunction.png)

4. Now, you'll want to change the three variables.

```Python
GAMING_INSTANCE_NAME = 'GamingRig'  # Replace this with the name of your server
GAMING_INSTANCE_REGION = 'eu-west-3' # Replace this with the region your server is in
GAMING_INSTANCE_SIZE_GB = 512  # Replace this with the size of your disk
```

5. The function will typically only run for a few seconds, however there is an exception. Snapshots in AWS are built incrementally, which is why they're so fast - except the first time we create a snapshot there's nothing to base on, so the entire 512GB volume needs to be snapshotted, which takes a while. It will also take a while to take a snapshot after installing a large game. So, we'll increase our function execution time limit. Scroll down to **Basic Settings** and click **Edit**, then set the **Timeout** to 15 minutes. Click **Save** when you're done. 

![Function timeout](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/functiontimeout.png)

6. Click **Deploy** to save the function. Next, we need to give our function permission to manage our EC2 resources. To do this, click on **Permissions** from the top, and click on the role that AWS automatically created for your function.

![Function role](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/functionrole.png)

7. Now click **Attach Policies**, search for **EC2** and choose the **AmazonEC2FullAccess** policy. Click **Attach Policy**

![EC2 full access](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ec2access.png)

8. At this point, you should **really** test that the function works. From the EC2 console, Terminate the instance (**Instance State > Terminate**). Then, back in Lambda, click **Test > Create Test Event** and give the event a name. Then click **Test** to see whether the function works. If it does, you should see output similar to the following (note that this will take a while):

![Lambda test success](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/testsuccess.png)

9. Next, we need to tell AWS to run this function every time our instance is terminated. Go to **Services > Amazon EventBridge**, then click **Create rule**. Fill in the form as follows:

- **Name:** Any name.
- **Description:** Any description.
- **Define Pattern:** Event Pattern.
- **Event matching pattern:** Pre-defined pattern by service.
- **Service provider:** AWS.
- **Service Name:** EC2.
- **Event Type:** EC2 Instance State-change Notification.
- **Specific state(s):** Checked, and choose **terminated** from the list of states.

9. Now from **Select targets**, and from the **Function** drop-down, choose the Lambda function we created earlier. Note that the function checks instance tags when doing its thing, so it won't mess around with your other instances/volumes/snapshots/AMIs.

![Event configuration](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/event1.png)

10. At this point, shutdown your gaming rig, then from the EC2 console choose **Actions > Terminate**. This will terminate the instance and the Lamda function should kick in, which will create the initial snapshot of the machine. You can monitor it from the **Snapshots** section of the EC2 console. Note that this initial snapshot will take a while to complete, but following this snapshots shouldn't take that long - it depends on how many changes you've made to the machine whilst using it. 

## Creating the Start Script

This section is also optional. Here we create a script that will automatically launch a gaming instance using spot pricing for us, without having to login to the AWS Console. 

1. Go to **Services > EC2 > Launch Templates**. Click **Create Launch Template**.

2. Now, you need configure the template with the following settings:

- **Launch template name:** Set any name here.
- **Template version description:** 1 
- **AMI:** Don't include in launch template.
- **Instance Type:** g4dn.xlarge (or whatever size you chose).
- **Key pair (login):** Choose the key you created when creating the instance.

3. Under **Storage (volumes)** click **Add new volume** with the following settings:

- **Size (GiB):** 512 (or whatever size you're using). 
- **Device name:** /dev/sda1 - you need to choose **Specify a custom value...** to be able to do this.
- **Volume type:** General purpose SSD (gp2)
- **Delete on termination:** No
- **Encrypted:** No

4. Under **Resource tags**, click **Add Tag** and create a tag with the Key set to **Name** and the Value set to the name of your gaming server (**GamingRig** in my case). Make sure that both **Instances** and **Volumes** are selected under **Resource Types**. Now click **Add Tag** again, and create a tag with the Key set to **SnapAndDelete** and the Value set to **True** - again making sure that both **Tag instances** and **Tag volumes** are enabled. Note that tag keys and values are CASE SENSITIVE.

![Launch tags](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/launchtags.png)

5. Expand **Advanced details**, then:

- **Request Spot Instances:** Checked.
- Click **Customize** then click **Set your maximum price (per instance/hour)** and set your price to some value greater than the instance average. You can see current average prices [here](https://aws.amazon.com/ec2/spot/pricing/) - make sure you choose your region. For example, the average in eu-west-3 is $0.37, so I set it to $0.40.
- **Shutdown behavior:** Terminate. 
- **Termination protection:** Disable.
- **Detailed CloudWatch monitoring:** Disable.
 
6. Phew! Finally, we can click **Create launch template**, followed by **View launch template**.

7. Now, you need to get the start script for your system. If you're using macOS or Linux, you need [start_server.sh](https://github.com/keithvassallomt/parsec-aws-automation/blob/master/start_server.sh). If you're using Windows, you need [start_server.ps1](https://github.com/keithvassallomt/parsec-aws-automation/blob/master/start_server.ps1). Add this script to **That Folder**.

8. Open the file you downloaded, and change the following if on Linux/macOS:

```Bash
GAMING_INSTANCE_NAME = "GamingRig"  # Replace this with the name of your server
LAUNCH_TEMPLATE = "lt-123434abcd"  # Replace this with the launch template ID
```

Or the following if on Windows:

```powershell
$GAMING_INSTANCE_NAME = "GamingRig"  # Replace this with the name of your server
$LAUNCH_TEMPLATE = "lt-123434abcd"  # Replace this with the launch template ID
```

To get your launch template ID easily, click on the launch template ID from the AWS Console:

![Launch template id 1](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/launchid1.png)

Now click the copy icon next to the launch template ID.

![Launch template id 2](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/launchid2.png)

9. If you're using Linux or macOS, you need to make the file executable. To do this, open a terminal (on macOS just search for **Terminal** from Spotlight or Applications > Utilities, on Linux - you should know how to do that already). Then, type:

```bash
cd /path/to/ThatFolder
chmod +x start_script.sh
```

Obviously replace the **/path/to/** part with the path to **That Folder**.

10. For the start script to work, you need to have the AWS CLI installed. If not, you can can install it on Windows from [Here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html), or macOS from [Here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html) or Linux from [Here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html). 

11. If you've just installed the AWS CLI you then need to configure it. Open a terminal on Linux or macOS, or open Command Prompt or PowerShell on Windows. Then type **aws configure**. You will be asked questions, answer as follows:

- **AWS Access Key ID:** The access key you used in step 9 of the **Installing Parsec** section. 
- **AWS Secret Access Key:** The secret key from the same step. Note that you should have stored these in **That Folder**.
- **Default region name:** The region where you set up your gaming server.
- **Default output format:** json.

![AWS Configure](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/awsconfigure.png)

## Putting it All Together

We're done! We can now take our server out for a spin, which will also let me explain exactly how to use this thing.

1. OK, so you're in the mood to kill some demons. The first thing you do is open a terminal on Linux/macOS or PowerShell on Windows. You then run the start script using **./start_script.sh** on Linux/macOS, or **start_script.ps1** on Windows.

![Tutorial 1](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial1.png)

2. When the instance is run, you will be shown the instance details. Press **q** to hide these.

![Tutorial 2](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial2.png)

3. At this point, open the Parsec client and just wait for your server to boot up. Following this you can connect to your server and game away.

![Tutorial 3](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial3.png)

4. Once you're done gaming, all you need to do is shutdown the server.

![Tutorial 4](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial4.png)

5. At this point, you can go ahead with your life. However, since this is the first time, let's use the AWS Console to see what's happening behind the scenes. After shutting down your server, from **Services > EC2 > Instances** we can see our instance is shutting down. After a short while it will change to the Terminated state.

![Tutorial 5](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial5.png)

6. If you go to **Snapshots**, you'll see that our script starts creating a snapshot.

![Tutorial 6](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial6.png)

7. After the snapshot is ready, going to the **Volumes** section shows that the volume has been deleted.

![Tutorial 7](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial7.png)

8. In the **Images** section, you'll see the brand new AMI, ready for your next gaming session.

![Tutorial 8](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tutorial8.png)

## Gaming
I installed Steam and Doom Eternal to gave it a shot.

![Killing a hell priest](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/doom.png)
