# 🚀 AWS Self-Healing Data Pipeline System

## 📌 Overview

This project implements a **fully automated, self-healing data pipeline** using AWS cloud services.
It detects failures, sends alerts, and automatically restarts the pipeline — without manual intervention.

---

## ⚙️ Architecture

CloudWatch → SNS → Lambda → SSM → EC2

---

## 🔧 Technologies Used

* AWS EC2
* AWS S3
* AWS Lambda
* AWS CloudWatch
* AWS SNS
* AWS Systems Manager (SSM)
* AWS SES (Email notifications)
* Python (Pandas, NumPy)
* Shell scripting

---

## 🚀 Features

* Automated data processing pipeline (200K+ records)
* Data cleaning and transformation using Pandas
* S3 integration for input/output data
* Real-time error detection using CloudWatch logs
* SNS email alerts for failures
* Intelligent Lambda restart logic (checks before restarting)
* Remote command execution via SSM
* Daily scheduled email reporting (7:00 AM) for both success and failure
* Retry logic for pipeline resilience
* CloudWatch dashboard for system monitoring

---

## 🧠 Key Achievements

* Built a **self-healing system** with zero manual intervention
* Improved reliability and fault tolerance
* Implemented intelligent decision logic in automation workflow
* Designed monitoring + alerting + recovery architecture

---

## 📁 Project Structure

```
aws-self-healing-data-pipeline/
├── pipeline/
│   ├── pipeline.py
│   ├── run_pipeline.sh
├── lambda/
│   └── restart_pipeline.py
├── requirements.txt
├── README.md
```

---

## 📊 How It Works

1. Pipeline runs on EC2 and processes data from S3
2. CloudWatch monitors logs for errors
3. If error occurs → SNS sends alert
4. Lambda is triggered
5. Lambda checks if pipeline is running
6. If not running → SSM restarts the pipeline
7. Email notification is sent for success or failure

---

## 🎯 Outcome

* Fully automated pipeline system
* No manual monitoring required
* Real-time error detection and recovery
* Production-level cloud architecture

---

## 👨‍💻 Author

**Paul Misheal**
