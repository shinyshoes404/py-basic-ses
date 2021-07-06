import click
from py_basic_ses.emailing import SESSender

@click.command()
@click.option("--to", default="", help="The address you want the email to be sent to.")
@click.option("--fromaddr", default="", help="The address you want the email to be from.")
@click.option("--awsregion", default="", help="AWS region your SES service is hosted in. Example: 'us-west-2'")
def send_test_email(to, fromaddr, awsregion):
    if not to or to=="":
        click.echo("You need to provide an email address.")
        if not fromaddr or fromaddr == "":
            click.echo("You need to provide a from address.")
            if not awsregion or awsregion == "":
                click.echo("You need to provide your AWS region.")
            
    else:
        click.echo("Attempting to send a test email to {0}".format(to))
     
        ses_send_obj = SESSender(sendto=to,fromaddr=fromaddr, message_txt="Test message from py-basic-ses",aws_region=awsregion)
        ses_send_obj.send_email()

@click.command()
@click.option("--emailaddr", default="", help="List the email you want to send to.")
@click.option("--message", default="", help="Provide the body of the email.")
def send_email(emailaddr, message):
    if not emailaddr or emailaddr=="":
        click.echo("You need to provide an email address.")
    else:
        if not message or message=="":
            click.echo("You need to provide the body of your email message.")        
        else:
            click.echo("Attempting to send an email to {0}".format(emailaddr))
            click.echo("With email message of {0}".format(message))

            ses_send_obj = SESSender(emailaddr,message)
            ses_send_obj.send_email()