FROM python:3.10-slim

WORKDIR /app

COPY pipeline/pipeline.py ./pipeline.py

RUN pip install pandas boto3 openpyxl

CMD ["python", "pipeline.py"]
