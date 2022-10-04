import unittest, mock
from click.testing import CliRunner

from py_basic_ses.entry import send_test_email, send_email


class TestEntrySendTestEmail(unittest.TestCase):

    def test_unit_send_test_email_no_sendto(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_test_email, '--fromaddr myaddress --awsregion myregion')
        print(test_result.output)
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_test_email_no_fromaddr(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_test_email, '--to youraddress --awsregion myregion')
        print(test_result.output)
        self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_no_awsregion(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress')
        print(test_result.output)
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_test_email_sessender_init_except(self):
        with mock.patch("py_basic_ses.entry.SESSender.__init__", side_effect=Exception("fake init exception")) as mock_sessender:
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_sessender_validate_except(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.side_effect = Exception("fake validate exception")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_sessender_validate_fail(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = False
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_sessender_send_exception(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = True
            mock_sessender.return_value.send_email.side_effect = Exception("send exception")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_sessender_send_fail(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = True
            mock_sessender.return_value.send_email.return_value = False
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_sessender_send_success(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = True
            mock_sessender.return_value.send_email.return_value = True
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 0)



class TestEntrySendEmail(unittest.TestCase):

    def test_unit_send_email_no_sendto(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
        print(test_result.output)
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_email_no_fromaddr(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--to youraddress --awsregion myregion --message_txt myplainmsg')
        print(test_result.output)
        self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_no_awsregion(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --message_txt myplainmsg')
        print(test_result.output)
        self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_no_msg(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
        print(test_result.output)
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_email_sessender_init_except(self):
        with mock.patch("py_basic_ses.entry.SESSender.__init__", side_effect=Exception("fake init exception")) as mock_sessender:
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_sessender_validate_except(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.side_effect = Exception("fake validate exception")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_sessender_validate_fail(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = False
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_sessender_send_exception(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = True
            mock_sessender.return_value.send_email.side_effect = Exception("send exception")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_sessender_send_fail(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = True
            mock_sessender.return_value.send_email.return_value = False
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_sessender_send_success(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.ses_validate.return_value = True
            mock_sessender.return_value.send_email.return_value = True
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            print(test_result.output)
            self.assertEqual(test_result.exit_code, 0)