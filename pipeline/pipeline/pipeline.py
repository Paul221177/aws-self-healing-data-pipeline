Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-1010-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri Apr 10 21:21:36 UTC 2026

  System load:  0.0               Processes:             110
  Usage of /:   49.0% of 6.71GB   Users logged in:       0
  Memory usage: 25%               IPv4 address for enX0: 172.31.32.58
  Swap usage:   0%

 * Ubuntu Pro delivers the most comprehensive open source security and
   compliance features.

   https://ubuntu.com/aws/pro

Expanded Security Maintenance for Applications is not enabled.

8 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


Last login: Fri Apr 10 18:44:34 2026 from 18.206.107.28
ubuntu@ip-172-31-32-58:~$ cat /home/ubuntu/pipeline.py
import pandas as pd
import boto3
from io import BytesIO
import logging
import traceback
import time

# =========================
# CONFIG
# =========================
BUCKET_NAME = "nsitf-data-misheal-001"
INPUT_KEY = "employers_clean (1).xlsx"
OUTPUT_KEY = "cleaned/employers_cleaned_ec2.csv"

SES_REGION = "us-east-1"
SENDER_EMAIL = "paulmisheal4@gmail.com"
RECIPIENT_EMAIL = "donprecident@gmail.com"

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 10

# =========================
# LOGGING SETUP
# =========================
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(message):
    print(message)
    logging.info(message)

# =========================
# EMAIL FUNCTION
# =========================
def send_email(subject, body):
    ses = boto3.client("ses", region_name=SES_REGION)
    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            "ToAddresses": [RECIPIENT_EMAIL]
        },
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Text": {"Data": body}
            }
        }
    )

# =========================
# MAIN PIPELINE
# =========================
def main():
    log("Starting pipeline...")

    s3 = boto3.client("s3")

    log("Downloading file from S3...")
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=INPUT_KEY)
    file_content = obj["Body"].read()
    excel_data = BytesIO(file_content)

    log("Reading Excel file...")
    df = pd.read_excel(excel_data)

    log("Cleaning column names...")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("__", "_", regex=False)
    )

    log("Cleaning phone columns...")
    for col in ["primary_no", "secondary_no"]:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype("int64").astype(str)

    log("Cleaning registered_date...")
    if "registered_date" in df.columns:
        df["registered_date"] = pd.to_datetime(
            df["registered_date"],
            errors="coerce",
            dayfirst=True
        )

    log("Saving CSV locally...")
    local_file = "cleaned_ec2.csv"
    df.to_csv(local_file, index=False)

    log("Uploading to S3...")
    s3.upload_file(local_file, BUCKET_NAME, OUTPUT_KEY)

    log(f"Pipeline completed successfully. Shape: {df.shape}")
    log(f"Uploaded to: s3://{BUCKET_NAME}/{OUTPUT_KEY}")

    send_email(
        subject="NSITF Pipeline Success",
        body=(
            f"Pipeline completed successfully.\n\n"
            f"Shape: {df.shape}\n"
            f"Uploaded to: s3://{BUCKET_NAME}/{OUTPUT_KEY}"
        )
    )

# =========================
# EXECUTION WITH RETRIES
# =========================
if __name__ == "__main__":
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log(f"Attempt {attempt} of {MAX_RETRIES}")
            main()
            log("Pipeline succeeded")
            break

        except Exception as e:
            error_message = str(e)

            logging.error(f"Attempt {attempt} failed")
            logging.error(error_message)
            logging.error(traceback.format_exc())

            if attempt == MAX_RETRIES:
                try:
                    send_email(
                        subject="NSITF Pipeline Failed",
                        body=(
                            f"Pipeline failed after {MAX_RETRIES} attempts.\n\n"
                            f"Error:\n{error_message}\n\n"
                            f"Check pipeline.log on EC2 for full details."
                        )
                    )
                    print("Pipeline failed after retries. Email alert sent.")
                except Exception as mail_error:
                    logging.error("Failed to send failure email")
                    logging.error(str(mail_error))
                    logging.error(traceback.format_exc())
                    print("Pipeline failed after retries. Email could not be sent.")
            else:
                print(f"Attempt {attempt} failed. Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
ubuntu@ip-172-31-32-58:~$ 
