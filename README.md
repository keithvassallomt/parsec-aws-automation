Parsec AWS Automation Scripts & Guide
=====================================

| Info        | Value           |
| ------------- |:-------------|
| Created by      | Keith Vassallo |
| Acknowledgements      | [/u/rom-ok](https://www.reddit.com/user/rom-ok)<br>[/u/dolanders](https://www.reddit.com/user/dolanders)<br>The [Parsec Team](https://parsecgaming.com/)      |
| Related Reading      | [Parsec AWS Guide](https://blog.parsecgaming.com/rtx-cloud-gaming-with-the-new-aws-g4-instances-11d1c60c2d09) |

## Table of Contents

**[Aims](#aims)**<br>
**[Setting up the Server](#setting-up-the-server)**<br>
**[Installing Parsec](#installing-parsec)**<br>
**[Creating the Automation Script](#creating-the-automation-script)**<br>
**[Creating the Start Script](#creating-the-start-script)**<br>

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
3. Optionally (but recommended), create a [Razer Account](https://aws.amazon.com/registration-confirmation/).
4. Download Microsoft Remote Desktop Client [for Windows](https://www.microsoft.com/en-us/p/microsoft-remote-desktop/9wzdncrfj3ps?activetab=pivot:overviewtab) or [for macOS](https://docs.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-mac)
4. Login to the [AWS Console](https://console.aws.amazon.com) using your root account.
5. Go to **Services > EC2**.
6. Click on **Running Instances**.

![Running instances](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/running_instances.png)

7. Choose a region closest to you (from the top right). 

![Region selection](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/region.png)

8. Click **Launch Instance**. You will want to select either **Windows Server 2016 Base** or **Windows Server 2019 Base**. I chose the 2016 option, but 2019 should also work fine.

![2016 Base](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/2016Base.png)

9. From the next screen, choose the **g4dn.xlarge** instance type. 

![g4dn.xlarge instance](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/g4dnxlarge.png)

10. Click **Next: Configure Instance Details**.

11. Click on **Request Spot Instances**. This will allocate resources to your system only when Amazon can spare them. Now, AWS has a **lot** of resources, so in reality I've never encountered an issue where I couldn't start an instance, or where my instance was terminated. This depends on the region you choose and the load at the time. You'll also want to enter a bid that's slightly higher than the average price, to increase your chances of getting an instance. **Note:** Sometimes AWS will ignore your maximum price, this is something I'm looking into. In the example below the average price is $0.37, so I entered a bid of $0.40, but my instances was charged at $0.79. Still, 79c an hour ain't bad!

![Requesting a spot instance](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/spot.png)

12. Leave all other options unchanged, and move on to **Next: Add Storage**. From here, you will need to choose how big you want your disk to be. I chose 512GB, since it's roomy and I typically don't leave all my games installed at once. Of course, you can choose any size you want here, but bear in mind you are charged per GB. Choose **General Purpose SSD (gp2)** as the storage type and make sure you turn **OFF** the **Delete on Termination** checkbox. This ensures our volume isn't destroyed when we shutdown our machine. We'll be creating a script to handle that part for us. 

![Adding storage](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/storage.png)

13. Move on to **Next: Add Tags**. This is **Very Important** so don't skip it. You'll want to create a tag called **Name** - with a capital **N**. For the value, choose a name for your gaming server. In this guide I'm just calling it **GamingRig**, but feel free to get creative here. Also make sure that the checkboxes for both **Instances** and **Volumes** are checked.

![Tagging the instance](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/tagginginstance.png)

14. Move on to **Next: Configure Security Group**. Leave the default option to create a new security group, and give it an easy-to-remember name, such as **Your_Instance_Name_Here-Sg**.

![Create security group](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/securitygroup.png)

15. Now click **Review and Launch** and click **Launch**. You'll be asked to create a key pair. Click **Create a new key pair** and give the key a name. 

![Create a key pair](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/createkeys.png)

16. **Download** the key and keep it somewhere safe. I strongly recommend you create a folder on your system to keep all documents related to your gaming rig. From now on, I'll refer to this as **That Folder**.

17. Finally, click **Launch Instances**. Now, one of two things will happen - either you'll get a message that your instance was launched successfully, or you'll get an error, like I did:

![Spot request error](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/spoterror.png)

If this happens, click **Retry Failed Tasks** to try again. This typically solves the problem.

18. Our instance has launched! To confirm, click **View Instances** and then click **Instances**. You'll see the instance is starting or has already started. 

![Instance started](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/instance_started.png)

19. Now we'll connect to the instance. With your instance selected, click **Connect**, then click **Download Remote Desktop File** and add it to **That Folder**. Next, click **Get Password**. If you get a warning about the password not being available yet, click **Try again** until it is. Browse to the location of your key file (it should be in **That Folder**). This will display the key contents in the window.

![Decrypted password](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/decrypted.png)

20. Click **Decrypt Password**. You will be shown the username (**Administrator**) and your password. Save these somewhere safe, I suggest in **That Folder** at first, but eventually move these to a proper password manager.

## Installing Parsec

We'll now install Parsec via their awesome script, which will also install other stuff to make our life easier, as well as update the GPU drivers.

1. Double-click on the RDP file you downloaded earlier, this will open a connection in Microsoft RDP Client, with the username already filled in. Simply paste the password and click **Connect**. You will connect to the desktop of the instance.

2. Now click **Start** and type **PowerShell**, click on **Windows PowerShell**. Now we need to get the Parsec setup script. Head on over to the [Parsec Cloud Preparation Tool GitHub](https://github.com/jamesstringerparsec/Parsec-Cloud-Preparation-Tool) and copy the script given:

![Parsec cloud prep tool](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/prepcopy.png)

3. Now, back in your RDP session, paste the script in PowerShell. This will extract a compress file. Press **Enter** to continue the process.

![Parsec cloud prep tool 1](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps1.png)

4. You will be asked whether to configure automatic Windows login. Type **Y** to accept this. You will be asked for your username and password, which you placed earlier in **That Folder**. 

![Parsec cloud prep tool 2](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps2.png)

5. Parsec will now install a bunch of stuff, including DirectX 11, Chrome, Parsec an d 7zip. When Parsec is installed, you'll see the Parsec client - go ahead and login. The login won't work at first, but you'll receive an e-mail asking you to confirm your location. Click on **Approve your new location** once you get the email, then login to Parsec on your gaming server.

6. Eventually you'll see a pop-up for Razer Synapse - asking you to login. According to Parsec you don't need to login here, but I was never able to get it to work without doing that. So just login with a Razer account. You'll soon see the Razer Surround sound app opened. Go ahead and close it. 

![Parsec cloud prep tool 3](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps3.png)

7. Now what's supposed to happen at this stage is that the Parsec script carries on, but in my experience, it doesn't. The only way I could get it to work is to right-click on the Razer Synapse software in the notification area in the Windows taskbar, and choose **Close Razer Synapse**. 

![Parsec cloud prep tool 4](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps4.png)

8. The Parsec script will now continue with the GPU updater tool. You'll be prompted to provide an Access Key and Secret. To do this, copy the link that is shown in the prompt, and paste it in your browser, or just [click here](https://console.aws.amazon.com/iam/home?/security_credentials#/security_credentials). 

![Parsec cloud prep tool 5](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps5.png)

9. Now click on **Access keys (access ID and secret access key)** and click **Create New Access Key**. Click **Download Key File** and add this to **That Folder**. Then click **Show Access Key** - this will show the access key and secret access key. Copy the first one and paste it in the PowerShell window, pressing **Enter**. Then copy the secret key and also paste it in PowerShell, followed by **Enter**. You'll be asked whether to save the access key - type **y**. Answer the next two questions with **y**.

![Parsec cloud prep tool 6](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/ps6.png)

10. When the driver is installed, you'll be advised that you don't need a reboot - but in my experience, you do. So, when asked to reboot, press **y** to reboot the system.

11. Use the steps outlined in step 1 to re-connect to your system via RDP.

12. At this point you should configure Parsec (double-click the Parsec icon on your desktop). I used the following settings:

- Host Settings
  - If you're on macOS, change **Resolution** to match the resolution of your personal system. You can find this out by clicking **Apple > About this Mac > Displays**. If you don't do this, connecting via Parsec will fail to change the resolution of the server to match your system. Windows/Linux users don't need to do this.
  - Increase the **Bandwidth Limit** to **50 Mbps**.
  - Set **H.265 (HEVC)** to **On**.
- Client Settings (not really required, but \_(ツ)_/¯)
  - Change **Resolution** to match your setting from above.
  - Set **H.265 (HEVC)** to **On**.
  
13. At this point, the Parsec client on your system should show the server as available.

![Parsec server found](https://github.com/keithvassallomt/parsec-aws-automation/raw/master/images/serverok.png)

14. Optionally, double-click on the **Setup Auto Shutdown** icon on your desktop. This will shutdown your system after a number of minutes if its idle, just in case you forget to do it yourself. When prompted, I set it to 45 minutes. 

