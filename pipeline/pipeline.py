import time
import logging

logging.basicConfig(level=logging.INFO)

def run_pipeline():
    print("Running pipeline...")

    # your actual pipeline logic here
    # example:
    print("CSV file created successfully")
    print("File uploaded to S3 successfully")

def main():
    retries = 3
    delay = 5  # seconds

    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt}...")
            run_pipeline()
            print("Pipeline completed successfully")
            return

        except Exception as e:
            logging.error(f"Error on attempt {attempt}: {e}")

            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retries failed. Raising error...")
                raise

if __name__ == "__main__":
    main()
