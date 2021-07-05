import boto3
from botocore.exceptions import ClientError

        # Note: In order for this to work you have to make your Amazon IAM credentials available
        # to the boto3 library. To this you have two options:
        #       Option 1) Create a credentials file in the following location with no extension
        #               On Windows - C:\Users\<yourUserName>\.aws\credentials
        #               On Linux, MacOS, or Unix - ~/.aws/credentials
        #
        #               Inside the credentials file add the following
        #                   [default]
        #                   aws_access_key_id = YOUR_AWS_ACCESS_KEY_ID
        #                   aws_secret_access_key = YOUR_AWS_SECRET_ACCESS_KEY
        #
        #               Where YOUR_AWS_ACCESS_KEY_ID is the ID for your IAM user
        #               and YOUR_AWS_SECRET_ACCESS_KEY is the secret for that IAM user
        #
        #       Option 2) Export these two environment variables
        #               AWS_ACCESS_KEY_ID
        #               AWS_SECRET_ACCESS_KEY
        #        


class SESSender:
    def __init__(self,sendto,message=""): 

        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        self.SENDER = "Promox Cloud <proxmox@cloud.alden.swilsycloud.com>"

        # Replace recipient@example.com with a "To" address. If your account 
        # is still in the sandbox, this address must be verified.
        self.RECIPIENT = sendto

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the 
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        #CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        self.AWS_REGION = "us-west-2"

        # The subject line for the email.
        self.SUBJECT = "Testing - backup_confirm_email"

        # The email body for recipients with non-HTML email clients.
        self.BODY_TEXT = message
                    
        # The HTML body of the email.
        self.BODY_HTML = message
        
        # """<html>
        # <head></head>
        # <body>
        # <h1>Amazon SES Test (SDK for Python)</h1>
        # <p>This email was sent with
        #     <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        #     <a href='https://aws.amazon.com/sdk-for-python/'>
        #     AWS SDK for Python (Boto)</a>.</p>
        # </body>
        # </html>
        #             """            

        # The character encoding for the email.
        self.CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        self.client = boto3.client('ses',region_name=self.AWS_REGION)

    def send_email(self):
        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        self.RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.CHARSET,
                            'Data': self.BODY_HTML,
                        },
                        'Text': {
                            'Charset': self.CHARSET,
                            'Data': self.BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': self.SUBJECT,
                    },
                },
                Source=self.SENDER,
                
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    