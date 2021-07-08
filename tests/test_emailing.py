import os, platform
import unittest, mock

# import the SESSender class, so we can test it
from py_basic_ses.emailing import SESSender

# Create a new class to run our tests which inherits from unittest's TestCase class
# seting the SESSender.ses_validate() method
class TestEmailingSESSenderSesValidate(unittest.TestCase):

    # missing sendto
    def test_no_sendto(self):
        # instantiate SESSender
        validation_obj = SESSender(fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")
    
    # missing fromaddr
    def test_no_fromaddr(self):
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", message_txt="some text", aws_region="us-west-2")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")
    
    # missing message_txt
    def test_no_message_text(self):
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", aws_region="us-west-2")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")
    
    # missing aws_region
    def test_no_aws_region(self):
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")

    # wrong operating system
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR":"randomness"}, clear=True ) # mocking a random environment variable to take advantage of the clear=True to clear out any other enviornment vars, notice this does not need to be passed into the test method
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Fake OS") # mocking the platform.system() method to return Fake OS
    def test_no_env_wrong_os(self,mock_platform_system):
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")

    # correct OS, no environment variables, no credentials path
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=False) # mock that the path we are looking for does not exist
    def test_no_env_no_cred(self, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")

    # correct OS, no environment variables, credentials path exists, credentials not a file
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=True) # mock that the path we are looking for does exist
    @mock.patch('py_basic_ses.emailing.os.path.isfile', return_value=False) # mock that the path is not a file
    def test_no_env_not_file(self,mock_os_path_isfile, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")

    # correct OS, no environment variables, credentials path exists, credentials is a file, we don't have read access to credentials
    @mock.patch.dict(os.environ, {"RANDOM_ENV_VAR" : "value"}, clear=True ) # clearing all environment variables except for the random one
    @mock.patch('py_basic_ses.emailing.platform.system', return_value="Linux") # mock platform.system() to return 'Linux'
    @mock.patch('py_basic_ses.emailing.os.path.expanduser', return_value="/home/myuser/.aws/credentials") # mock os.path.expanduser() to return a filepath
    @mock.patch('py_basic_ses.emailing.os.path.exists', return_value=True) # mock that the path we are looking for does exist
    @mock.patch('py_basic_ses.emailing.os.path.isfile', return_value=True) # mock that the path is a file
    @mock.patch('py_basic_ses.emailing.os.access', return_value=False) # mock that we do not have read access to credentials
    def test_no_env_no_access(self,mock_os_access, mock_os_path_isfile, mock_os_path_exists, mock_expanduser, mock_platform_system): # notice the arguments are in bottom to top order of decorators
        # instantiate SESSender
        validation_obj = SESSender(sendto="email@domain.com", fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
        check_validation = validation_obj.ses_validate()
        # expecting False to be returned
        self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")

    


# run the main() method from the unittest module
if __name__ == "__main__":
    unittest.main()
