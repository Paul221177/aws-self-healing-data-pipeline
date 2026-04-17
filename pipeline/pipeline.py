import pandas as pd
import boto3

# Create sample data
data = {
    "name": ["Paul", "John", "Mary"],
    "age": [25, 30, 22]
}

df = pd.DataFrame(data)

# Save file
file_path = "/tmp/output.csv"
df.to_csv(file_path, index=False)

print("CSV file created successfully")

# Upload to S3
s3 = boto3.client("s3")

bucket_name = "nsitf-data-misheal-001"
s3.upload_file(file_path, bucket_name, "output.csv")

print("File uploaded to S3 successfully")
1/0
