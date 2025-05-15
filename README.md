# AWS Streamlit Deployment Guide

Deploy a Streamlit app on AWS EC2 with Auto Scaling, Load Balancer (ALB), and Custom VPC

The Dashboard: 
![image](https://github.com/user-attachments/assets/966fbf83-6efe-45d7-a6c2-f028fd4660a5)

📌 Table of Contents
Project Overview

Prerequisites

Step 1: Prepare Your Streamlit App

Step 2: Set Up AWS Infrastructure

Create a Custom VPC

Configure Subnets

Set Up Security Groups

Step 3: Deploy Streamlit on EC2

Launch Template

Auto Scaling Group (ASG)

Application Load Balancer (ALB)

Step 4: Access Your App

Troubleshooting

Optional Enhancements

Architecture Diagram

🌐 Project Overview
Deploy a scalable Streamlit app on AWS with:
✅ Custom VPC (Isolated network)
✅ Auto Scaling (Handles traffic spikes)
✅ Load Balancer (Distributes traffic)
✅ HTTPS (Optional) (Secure access)

![Project Architecture](https://github.com/user-attachments/assets/f77c5482-47ea-4a2f-9f26-b8e371651c5c)

📋 Prerequisites
AWS Account (Sign up here)

Streamlit App Files (app.py, requirements.txt, dataset)

Basic CLI Knowledge (PowerShell/Git Bash)

🚀 Step 1: Prepare Your Streamlit App
File Structure

my-streamlit-app/  
├── app.py          # Streamlit script  
├── requirements.txt # Dependencies  
└── data.csv        # Dataset  

Example requirements.txt

streamlit  
pandas  
numpy  

🛠️ Step 2: Set Up AWS Infrastructure
🔹 A. Create a Custom VPC
Go to VPC Console → Your VPCs → Create VPC.

Configure:

Name: streamlit-vpc

IPv4 CIDR: 10.0.0.0/16

B. Configure Subnets
Create 2 public subnets (different AZs for high availability):

streamlit-subnet-1 → 10.0.1.0/24 (us-east-1a)

streamlit-subnet-2 → 10.0.2.0/24 (us-east-1b)

Enable auto-assign public IPv4 for each subnet.

🔹 C. Set Up Security Groups
For EC2 Instances:

Allow SSH (port 22) from your IP.

Allow HTTP (port 8501) from the ALB security group.

For ALB:

Allow HTTP (port 80) from 0.0.0.0/0.

⚡ Step 3: Deploy Streamlit on EC2
🔹 A. Launch Template
Go to EC2 → Launch Templates → Create.

Configure:

AMI: Amazon Linux 2

Instance Type: t2.micro (free tier)

Key Pair: Create/download .pem file

User Data (Paste this script):

#!/bin/bash
yum update -y
yum install -y python3 pip
pip3 install streamlit pandas numpy
mkdir /home/ec2-user/streamlit-app
cd /home/ec2-user/streamlit-app
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &

 B. Auto Scaling Group (ASG)
Go to EC2 → Auto Scaling Groups → Create.

Attach to the ALB and set:

Min/Max Instances: 1/2

Scaling Policy: CPU > 50%

🔹 C. Application Load Balancer (ALB)
Create an Internet-facing ALB.

Configure:

Listener: HTTP (port 80) → Forward to target group (streamlit-target-group).

Health Checks: HTTP:8501, path /

Step 4: Access Your App
Via ALB DNS: http://streamlit-alb-825879435.eu-west-3.elb.amazonaws.com
Via EC2 Public IP: http://35.180.247.37:8501/

🐞 Troubleshooting
Issue	Fix
ALB shows "unhealthy"	Check curl http://localhost:8501 on EC2
Port 8501 in use	Run pkill -f "streamlit run"
SSH permission denied	Run icacls key.pem /reset (Windows)

🚀 Optional Enhancements
HTTPS: Add SSL via AWS ACM.

Domain: Point a custom domain (e.g., app.example.com) to the ALB.

CI/CD: Auto-deploy with GitHub Actions.

📜 Final Notes
Cost: Monitor with AWS Cost Explorer.

Backups: Use S3 for dataset backups.

Congratulations! Your app is now live and scalable. 🎉

📎Attachments
Sample-app.py:
![image](https://github.com/user-attachments/assets/c3d93276-8f19-47c6-a415-b5cf6f164c56)

