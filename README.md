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

20. 

## Installing Parsec
