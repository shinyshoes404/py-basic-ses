import click
from py_basic_ses.emailing import SESSender

@click.command()
@click.option("--emailaddr", default="", help="List the email you want to send to.")
def send_test_email(emailaddr):
    if not emailaddr or emailaddr=="":
        click.echo("You need to provide an email address.")
    else:
        click.echo("Attempting to send a test email to {0}".format(emailaddr))
     
        ses_send_obj = SESSender(emailaddr, "Testing our application.")
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