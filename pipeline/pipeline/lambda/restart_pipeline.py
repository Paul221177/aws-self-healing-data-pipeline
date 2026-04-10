import json
import time
import boto3

ssm = boto3.client("ssm")

INSTANCE_ID = "i-003133c59d18c18cc"

def lambda_handler(event, context):
    try:
        check_response = ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    "pgrep -f pipeline.py >/dev/null && echo RUNNING || echo NOT_RUNNING"
                ]
            },
            Comment="Check if pipeline is running"
        )

        check_command_id = check_response["Command"]["CommandId"]

        time.sleep(3)

        check_result = ssm.get_command_invocation(
            CommandId=check_command_id,
            InstanceId=INSTANCE_ID
        )

        output = check_result.get("StandardOutputContent", "").strip()

        if "RUNNING" in output:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Pipeline already running. No restart needed.",
                    "check_command_id": check_command_id,
                    "check_output": output
                })
            }

        restart_response = ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    "cd /home/ubuntu",
                    "pkill -f pipeline.py || true",
                    "nohup bash run_pipeline.sh > pipeline.log 2>&1 &"
                ]
            },
            Comment="Restart pipeline via SSM"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Pipeline was not running. Restart command sent.",
                "check_command_id": check_command_id,
                "restart_command_id": restart_response["Command"]["CommandId"],
                "check_output": output
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Lambda failed",
                "error": str(e)
            })
        }
