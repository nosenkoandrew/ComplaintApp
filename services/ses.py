import boto3
from decouple import config
from fastapi import HTTPException


class SESService:
    def __init__(self):
        self.key = config('AWS_ACCESS_KEY')
        self.secret = config('AWS_SECRET')
        self.bucket = config('AWS_BUCKET_NAME')
        self.ses = boto3.client(
            "ses", region_name=config("SES_REGION"), aws_access_key_id=self.key, aws_secret_access_key=self.secret
        )
        self.region = config("AWS_REGION")

    def send_email(self, subject, to_addresses, text_data):
        body = {"Text": {"Data": text_data, "Charset": "UTF-8"}}
        self.ses.send_email(Source="nosenkoandrii.s@gmail.com",
                            Destination={"ToAddresses": to_addresses, "CcAddresses": [], "BccAddresses": []},
                            Message={"Subject": {"Data": subject, "Charset": "UTF-8"}, "Body": body})
