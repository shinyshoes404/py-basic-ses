# py-basic-ses
py-basic-ses provides a command line application and library to send emails via Amazon Web Services' Simple Email Service, or AWS SES, API by leveraging the boto3 library.

## AWS SES

AWS's Simple Email Service (SES) allows email to be sent from your custom domain without the hassle or barriers of setting up a mail server (I've tried this a couple of times, and it is a huge pain to do on a small scale). SES provides support for DKIM (helps you land in the inbox, rather than the spam folder) and custom MAIL FROM address (the envelope sender/return path will be your domain rather than @us-west-2.amazonses.com).

In order to use the py-basic-ses application or library, you do have to setup the SES service in your AWS account. You will need to obtain your IAM AWS access ID and secret key, and set the appropriate policies. More information on setting up SES and retrieving your required credentials can be found in the **Setting up SES, IAM users, credentials, and policies** section of this README.

You can learn more about AWS SES <a href='https://aws.amazon.com/ses/'>here</a>.

## Command line application

With py-basic-ses installed you will have two commands available from the terminal: `send-test` and `send-email`. `send-test --help` and `send-email --help` will display the availale options with explanations.

Assuming SES, credentials, and policies are setup as described in the **Setting up SES, IAM users, credentials, and policies** section of this README, below are examples of commands for sending a test email and sending a production email.  
<br>
**Sending a test email**  
```
send-test --to to-user@to-domain.com --fromaddr from-user@from-domain.com --awsregion your-aws-region
```  
Where `your-aws-region` is the region your SES service is operating in. An example would be `us-west-2`.  
<br>
**Sending a production email**  
```
send-email --to to-user@to-domain.com --fromaddr from-user@from-domain.com --fromname 'From User' --awsregion your-aws-region --subject 'Email Subject' --message_txt 'Email plain text message' --message_html '<h1>HTML Email Heading</h1><p>Email html message</p>'
```
Where `your-aws-region` is the region your SES service is operating in. An example would be `us-west-2`.  
The above command will send a two part message with html as the primary email body, and a plain text alternative email body. If only `--message_txt` is provided, the plain text will be put in both the html and plain text sections of the email. Not all arguments are required. Run the `send-email --help` command to see the list of arguments, and whether they are required or optional.

## Library
