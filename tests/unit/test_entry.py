import unittest, mock
from click.testing import CliRunner
from py_basic_ses.entry import send_test_email, send_email
from py_basic_ses.exceptions import CredError
from botocore.exceptions import ClientError


class TestEntrySendTestEmail(unittest.TestCase):

    def test_unit_send_test_email_no_sendto(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_test_email, '--fromaddr myaddress --awsregion myregion')
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_test_email_no_fromaddr(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_test_email, '--to youraddress --awsregion myregion')
        self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_no_awsregion(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress')
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_test_email_sessender_init_except(self):
        with mock.patch("py_basic_ses.entry.SESSender.__init__", side_effect=Exception("fake init exception")) as mock_sessender:
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_test_email_sessender_send_crederror(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = CredError("fake cred error")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            self.assertEqual(test_result.exit_code, 2)

    def test_unit_send_test_email_sessender_send_oserror(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = OSError("fake os error")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            self.assertEqual(test_result.exit_code, 3)

    def test_unit_send_test_email_sessender_send_clienterror(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = ClientError({"Error": {"Message":"fake resp"}}, "fake op name")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            self.assertEqual(test_result.exit_code, 4)

    def test_unit_send_test_email_sessender_send_unexpected_exception(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = Exception("fake exception")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            self.assertEqual(test_result.exit_code, 5)

    def test_unit_send_test_email_sessender_send_success(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.return_value = {"MessageId":"fakemsgID"}
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_test_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
            self.assertEqual(test_result.exit_code, 0)



class TestEntrySendEmail(unittest.TestCase):

    def test_unit_send_email_no_sendto(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_email_no_fromaddr(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--to youraddress --awsregion myregion --message_txt myplainmsg')
        self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_no_awsregion(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --message_txt myplainmsg')
        self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_no_msg(self):
        test_runner = CliRunner()
        test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion')
        self.assertEqual(test_result.exit_code, 1)
    
    def test_unit_send_email_sessender_init_except(self):
        with mock.patch("py_basic_ses.entry.SESSender.__init__", side_effect=Exception("fake init exception")) as mock_sessender:
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            self.assertEqual(test_result.exit_code, 1)

    def test_unit_send_email_sessender_send_crederror(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = CredError("fake cred error")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            self.assertEqual(test_result.exit_code, 2)

    def test_unit_send_email_sessender_send_oserror(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = OSError("fake os error")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            self.assertEqual(test_result.exit_code, 3)

    def test_unit_send_email_sessender_send_clienterror(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = ClientError({"Error": {"Message":"fake resp"}}, "fake op name")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            self.assertEqual(test_result.exit_code, 4)

    def test_unit_send_email_sessender_send_unexpected_exception(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.side_effect = Exception("fake exception")
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            self.assertEqual(test_result.exit_code, 5)

    def test_unit_send_email_sessender_send_success(self):
        with mock.patch("py_basic_ses.entry.SESSender") as mock_sessender:
            mock_sessender.return_value.send_email.return_value = {"MessageId":"fakemsgID"}
            test_runner = CliRunner()
            test_result = test_runner.invoke(send_email, '--to youraddress --fromaddr myaddress --awsregion myregion --message_txt myplainmsg')
            self.assertEqual(test_result.exit_code, 0)