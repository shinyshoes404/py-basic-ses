import boto3
from py_basic_ses.exceptions import CredError
import os, platform

class SESSender:
    def __init__(self,sendto: str, fromaddr: str, message_txt: str, aws_region: str, fromname: str = None, msgsubject: str = None, message_html: str = None):
        # set instance variables based on what was passed into __init__()
        self.sendto = sendto
        self.fromaddr = fromaddr
        self.message_txt = message_txt
        self.aws_region = aws_region
        self.fromname = fromname
        self.msgsubject = msgsubject
        self.message_html = message_html

    
    def ses_validate(self):
        # Returning False indicates an error. Returning True indicates everything was validated.
      
        # ---- AWS Credentials Validations ----        
        # Check for environment variables first
        if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
            return True
        
        # Since we don't have the environment variables we need present, we will need to use a credentials file
        # Start by determining the OS of the system running this application to determine the expected path to
        # the credentials file.                      
        # If the OS is not Linux or Windows, raise exception and stop routine.
        if platform.system() != "Linux" and platform.system() != "Windows":
            raise OSError("unrecognized operating system. py-basic-ses supports Windows or Linux")

        # determine the expected path to the credentials file based on the operating system
        if platform.system() == "Linux":
            # using expanduser() method to convert ~ into /home/<username>
            self.credpath = os.path.expanduser("~/.aws/credentials")
                    
        if platform.system() == "Windows":
            self.credpath = "C:\\Users\\" + os.getlogin() + "\\.aws\\credentials"

        
        # since no environment variables, does the cred file path exist? If not, raise an exception
        if not os.path.isfile(self.credpath):
            raise CredError(f'missing aws ses credentials, no env vars or file at {self.credpath}, for help setting up aws ses credentials see https://github.com/shinyshoes404/py-basic-ses#readme')

        else:
            # do we have read access on the credentials file?
            if os.access(self.credpath, os.R_OK) == False:
                raise CredError('cannot access credentials file, the file exists and is in the correct location, but this application does not have permission to read, for help setting up aws ses credentials see https://github.com/shinyshoes404/py-basic-ses#readme')

            else:
                # Read the contents of the file and look for aws_access_key_id and aws_secret_access_key
                # Remove any spaces in our string variable to prep for the .find() method.
                # In the credentials file, there can be as many spaces as you want between the key = value, but we need
                # to make sure that the key and = are present. If they are not, then the boto3 library will throw an error
                with open(self.credpath, "r") as cred_file:
                    cred_content = cred_file.read().replace(" ","")
                    
                # look for aws_access_key_id= and aws_secret_access_key=
                if cred_content.find("aws_access_key_id=") != -1 and cred_content.find("aws_secret_access_key=") != -1 and cred_content.find("[default]") != -1:
                    return True
                else:
                    raise CredError('malformed credentials file, for help setting up aws ses credentials see https://github.com/shinyshoes404/py-basic-ses#readme')
        
        

    def send_email(self) -> str:
        # make sure we have all of the required parameters before attempting to send an email
        self.ses_validate()

        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        # if a fromname was provided build out 'Sender Name <senderaddr@email.com>' format
        if self.fromname == None or self.fromname == "":
            self.SENDER = self.fromaddr
        else:
            self.SENDER = self.fromname + " <" + self.fromaddr + ">"        

        # Replace recipient@example.com with a "To" address. If your account 
        # is still in the sandbox, this address must be verified.
        self.RECIPIENT = self.sendto
        
        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        self.AWS_REGION = self.aws_region

        # The subject line for the email.
        if self.msgsubject == None:
            self.SUBJECT = ""
        else:
            self.SUBJECT = self.msgsubject

        # The email body for recipients with non-HTML email clients.
        self.BODY_TEXT = self.message_txt
                    
        # The HTML body of the email.
        if self.message_html == None:
            self.BODY_HTML = self.message_txt
        else:
            self.BODY_HTML = self.message_html                        

        # The character encoding for the email.
        self.CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        self.client = boto3.client('ses',region_name=self.AWS_REGION)


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


        return response['MessageId']

    