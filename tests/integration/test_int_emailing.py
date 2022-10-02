# import unittest, mock

# # import the SESSender class, so we can test it
# from py_basic_ses.emailing import SESSender

# # Real integration test using live credentials stored in the 
# class TestEmailingSESSenderSesValidate(unittest.TestCase):

#     # missing sendto
#     def test_no_sendto(self):
#         # instantiate SESSender
#         validation_obj = SESSender(fromaddr="email@domain.com", message_txt="some text", aws_region="us-west-2")
#         check_validation = validation_obj.ses_validate()
#         # expecting False to be returned
#         self.assertEqual(check_validation, False, "SESSender.ses_validate: expecting false")