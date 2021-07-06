import boto3
from botocore.exceptions import ClientError
import os, platform

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
        #               
        #        


class SESSender:
    def __init__(self,sendto=None, fromaddr=None, message_txt=None, aws_region=None, fromname=None, msgsubject=None, message_html=None):
       # Initialize check variable for credentials
        self.aws_creds_present = False 

        # --- Class argument validation ---
        # only the arguments checked below are required.
        self.required_args_present = False
        if sendto == None:
            print("Error: Missing send to address in the SESSender class")
            return
        if fromaddr == None:
            print("Error: Missing fromaddr in the SESSender class.")
            return
        
        if message_txt == None:
            print("Error: Missing message_txt in the SESSender class.")
            return
        
        if aws_region == None:
            print("Error: aws_region is missing in the SESSender class.")
            return
        
        # if we made it this far, all of our required arguments are present
        self.required_args_present = True

        # ---- AWS Credentials Validations ----        
        # Check for environment variables first
        if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
            self.aws_creds_present = True
                      
        # If the environment variables are present, no need to check for the credentials file
        if self.aws_creds_present == False:

            # store some messages to use later
            cred_instructions_msg = ("\nYou need to either set environment variables for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY,"
                                    " or create a file with these keys and their corresponding values at \n")
            cred_readme_msg = ("\nFor help setting up IAM users on AWS, retrieving credentials, and setting policies, "
                            "checkout the README for py-basic-ses at https://git.swilsycloud.com/useful-apps-and-libraries/py-basic-ses.")
            
            # If the OS is not Linux or Windows, print error and bail stop routine.
            if platform.system() != "Linux" and platform.system() != "Windows":
                print("\nError: We don't recognize your operating system. py-basic-ses supports Windows or Linux.")
                return

            # now check for the credentials file
            if platform.system() == 'Linux':
                self.credpath = os.path.expanduser("~/.aws/credentials")
            
            if platform.system() == "Windows":
                self.credpath = "C:\\Users\\" + os.getlogin() + "\\.aws\\credentials"

            
            # does the path exist?
            if os.path.exists(self.credpath) == False:
                # if not, print a helpful error message, and bail out of this routine.
                print("\nError: There is a problem with your AWS credentials.")
                print(cred_instructions_msg + self.credpath)
                print(cred_readme_msg)
                return
            else:
                # is credentials a file?
                if os.path.isfile(self.credpath) == False:
                    # if not, print a helpful error message and bail out of this routine.
                    print("\nError: There is a problem with your AWS credentials.")
                    print(self.credpath + " is not a file.")
                    print(cred_instructions_msg + self.credpath)
                    print(cred_readme_msg)
                    return

                else:
                    # do we have read access on the credentials file?
                    if os.access(self.credpath, os.R_OK) == False:
                        # if not, print a helpful error message and bail out of this routine.
                        print("\nError: Your credentials file exists, and is in the right place, but you don't have access to read its contents. Please fix this permissions issue.")
                        print(cred_instructions_msg + self.credpath)
                        print(cred_readme_msg)
                        return
                    else:
                        # read the contents of the file and look for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
                        with open(self.credpath, "r") as cred_file:
                            cred_content = cred_file.read()
                            if cred_content.find("AWS_ACCESS_KEY_ID=") != -1 and cred_content.find("AWS_SECRET_ACCESS_KEY=") != -1:
                                self.aws_creds_present = True
                            else:
                                print("\nError: Your credentials file is missing something we need.")
                                print("Your credentials file is missing either AWS_ACCESS_KEY_ID= or AWS_SECRET_ACCESS_KEY= \n")
                                print(cred_instructions_msg + self.credpath)
                                print(cred_readme_msg)
                                return                            


        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        # if a fromname was provided build out 'Sender Name <senderaddr@email.com>' format
        if fromname == None or fromname == "":
            self.SENDER = fromaddr
        else:
            self.SENDER = fromname + " <" + fromaddr + ">"        

        # Replace recipient@example.com with a "To" address. If your account 
        # is still in the sandbox, this address must be verified.
        self.RECIPIENT = sendto

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the 
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        #CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        self.AWS_REGION = aws_region

        # The subject line for the email.
        if msgsubject == None:
            self.SUBJECT = ""
        else:
            self.SUBJECT = msgsubject

        # The email body for recipients with non-HTML email clients.
        self.BODY_TEXT = message_txt
                    
        # The HTML body of the email.
        if message_html == None:
            self.BODY_HTML = ""
        else:
            self.BODY_HTML = message_html                        

        # The character encoding for the email.
        self.CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        self.client = boto3.client('ses',region_name=self.AWS_REGION)
        

    def send_email(self):

        # check for AWS cred flag
        if self.aws_creds_present == False and self.required_args_present == False:
            # if credentials have not ben validated, print error message and stop routine.
            print("Error: You did not instantiate the SESSender clsss correctly, and you need to fix your credentials before trying to send an email.")
            return
        
        if self.aws_creds_present == False:
            print("Error: You need to fix your credentials before trying to send an email.")
            return
        
        # check required arguments flag
        if self.required_args_present == False:
            print("Error: You are missing required arguments to instantiate the SESSender class.")
            return

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

    