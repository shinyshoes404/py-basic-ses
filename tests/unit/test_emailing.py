import os, unittest, mock
import boto3
from botocore.stub import Stubber
from botocore.exceptions import ClientError
from py_basic_ses.exceptions import CredError

# import the SESSender class, so we can test it
from py_basic_ses.emailing import SESSender

# Testing the SESSender.ses_validate() method
class TestEmailingSESSenderSesValidate(unittest.TestCase):

    # missing sendto
    def test_unit_ses_validate_no_sendto(self):
        with self.assertRaises(TypeError):
            SESSender(fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")

   
    # missing fromaddr
    def test_unit_ses_validate_no_fromaddr(self):
        with self.assertRaises(TypeError):
            SESSender(sendto="email@domain.com", message_txt="some text", aws_region="us-west-2")

    
    # missing message_txt
    def test_unit_ses_validate_no_message_text(self):
        with self.assertRaises(TypeError):
            SESSender(sendto="email@domain.com", fromaddr="email@domain.com", aws_region="us-west-2")
    
    # missing aws_region
    def test_unit_ses_validate_no_aws_region(self):
        with self.assertRaises(TypeError):
            SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text")


    # wrong operating system
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR":"randomness"}, clear=True ) # mocking a random environment variable to take advantage of the clear=True to clear out any other enviornment vars, notice this does not need to be passed into the test method
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Fake OS") # mocking the platform.system() method to return Fake OS
    def test_unit_ses_validate_no_env_wrong_os(self,mock_platform_system):
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        with self.assertRaises(OSError):
            validation_obj.ses_validate()


    # correct OS, no environment variables, no credentials path
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=False) # mock that the path we are looking for does not exist
    def test_unit_ses_validate_no_env_no_cred(self, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        with self.assertRaises(CredError):
            validation_obj.ses_validate()

    # correct OS, no environment variables, credentials path exists, credentials not a file
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=True) # mock that the path we are looking for does exist
    @mock.patch('py_basic_ses.emailing.os.path.isfile', return_value=False) # mock that the path is not a file
    def test_unit_ses_validate_no_env_not_file(self,mock_os_path_isfile, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        with self.assertRaises(CredError):
            validation_obj.ses_validate()


    # correct OS, no environment variables, credentials path exists, credentials is a file, we don't have read access to credentials
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=True) # mock that the path we are looking for does exist
    @mock.patch('py_basic_ses.emailing.os.path.isfile', return_value=True) # mock that the path is a file
    @mock.patch('py_basic_ses.emailing.os.access', return_value=False) # mock that we do not have read access to credentials
    def test_unit_ses_validate_no_env_no_access(self,mock_os_access, mock_os_path_isfile, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        with self.assertRaises(CredError):
            validation_obj.ses_validate()


    # correct OS, no environment variables, credentials path exists, credentials is a file, we have read access, the credentials file does not have the info we need
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=True) # mock that the path we are looking for does exist
    @mock.patch('py_basic_ses.emailing.os.path.isfile', return_value=True) # mock that the path is a file
    @mock.patch('py_basic_ses.emailing.os.access', return_value=True) # mock that we do have read access to credentials
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="string with no aws cred info") # mock the builtin open function to read in a string with no aws credentials info
    def test_unit_ses_validate_no_env_no_cred_info(self, mock_file_open, mock_os_access, mock_os_path_isfile, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        with self.assertRaises(CredError):
            validation_obj.ses_validate()


    # correct OS, no environment variables, credentials path exists, credentials is a file, we have read access, the credentials file has everything we are looking for
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=True) # mock that the path we are looking for does exist
    @mock.patch('py_basic_ses.emailing.os.path.isfile', return_value=True) # mock that the path is a file
    @mock.patch('py_basic_ses.emailing.os.access', return_value=True) # mock that we do have read access to credentials
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="[default]  \naws_secret_access_key  = BKIAYPKAJ70YPSLMJ9BZ \n aws_access_key_id   = 7GRwZHFWy8DHpqNXZTgcvSaY/T9/nZ+6Xm1E9FxS") # mock the builtin open function to read in a string with aws credentials info
    def test_unit_ses_validate_no_env_with_cred_file(self, mock_file_open, mock_os_access, mock_os_path_isfile, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        # expecting True to be returned
        self.assertEqual(validation_obj.ses_validate(), True, "SESSender.ses_validate: expecting True")

    
    # correct OS, with environment variables, credentials path does no exist
    @mock.patch.dict(os.environ, {"AWS_ACCESS_KEY_ID" : "BKIAYPKAJ70YPSLMJ9BZ", "AWS_SECRET_ACCESS_KEY" : "7GRwZHFWy8DHpqNXZTgcvSaY/T9/nZ+6Xm1E9FxS"}, clear=True ) # clearing all environment variables except for the AWS SES ones we need
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=False) # mock that the path we are looking for does not exist    
    def test_unit_ses_validate_with_env_no_cred_file(self, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        # expecting True to be returned
        self.assertEqual(validation_obj.ses_validate(), True, "SESSender.ses_validate: expecting True")


# Testing the SESSender.send_email() method
class TestEmailingSESSenderSendEmail(unittest.TestCase):
    
    def test_unit_send_email_ses_validate_exception(self):
        with mock.patch("py_basic_ses.emailing.SESSender.ses_validate", side_effect=Exception("fake validate exception")) as mock_sesvalidate:
            validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
            with self.assertRaises(Exception):
                validation_obj.send_email()
  
    def test_unit_send_email_boto3_init_exception(self):
        with mock.patch("py_basic_ses.emailing.SESSender.ses_validate", return_value=True) as mock_sesvalidate:
            with mock.patch("py_basic_ses.emailing.boto3.client", side_effect=Exception("fake boto3 exception")) as mock_botoclient:
                validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2", msgsubject="fake subject")
                with self.assertRaises(Exception):
                    validation_obj.send_email()

    def test_unit_send_email_clienterror_exception(self):
        stubbed_client = boto3.client('ses', region_name='us-west-2')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error('send_email')
        stubber.activate()
        with mock.patch("py_basic_ses.emailing.SESSender.ses_validate", return_value=True) as mock_sesvalidate:
            with mock.patch("py_basic_ses.emailing.boto3.client") as mock_botoclient:
                mock_botoclient.return_value = stubbed_client
                validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2", message_html="<p>fake html</p>")
                with self.assertRaises(ClientError):
                    validation_obj.send_email()                    

    def test_unit_send_email_unexpected_exception(self):
        with mock.patch("py_basic_ses.emailing.SESSender.ses_validate", return_value=True) as mock_sesvalidate:
            with mock.patch("py_basic_ses.emailing.boto3.client") as mock_botoclient:
                mock_botoclient.return_value.send_email.side_effect = Exception("fake unexpected exception")
                validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2", fromname="fake name")
                with self.assertRaises(Exception):
                    validation_obj.send_email()


    def test_unit_send_email_sends(self):
        with mock.patch("py_basic_ses.emailing.SESSender.ses_validate", return_value=True) as mock_sesvalidate:
            with mock.patch("py_basic_ses.emailing.boto3.client") as mock_botoclient:
                mock_botoclient.return_value.send_email.return_value = {"MessageId":"fakemsgID"}
                validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
                self.assertEqual(validation_obj.send_email(), "fakemsgID")


