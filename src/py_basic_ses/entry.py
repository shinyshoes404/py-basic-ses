import click, sys
from py_basic_ses.emailing import SESSender

@click.command()
@click.option("--to", default="", help="Address you are sending to. Required")
@click.option("--fromaddr", default="", help="Address you want the email to be from. Required")
@click.option("--awsregion", default="", help="AWS region your SES service is hosted in. Required")
def send_test_email(to, fromaddr, awsregion):
    if not to or to=="":
        click.echo("You need to provide an email address to send to.")
        sys.exit(1)
    if not fromaddr or fromaddr == "":
        click.echo("You need to provide a from address.")
        sys.exit(1)
    if not awsregion or awsregion == "":
        click.echo("You need to provide your AWS region.")
        sys.exit(1)

    try:              
        # instantiate the object
        ses_send_obj = SESSender(sendto=to,fromaddr=fromaddr, message_txt="Test message from py-basic-ses",aws_region=awsregion,msgsubject="Test py-basic-ses")
    except Exception as e:
        click.echo("unexpected exception")
        click.echo(e)
        sys.exit(1)
    
    try:
        # validate the arguments and credentials
        check_validation = ses_send_obj.ses_validate()
        if check_validation == False:
            sys.exit(1)
    except Exception as e:
        click.echo("unexpected exception")
        click.echo(e)
        sys.exit(1)

    # if everything validated, try to send the email
    click.echo("Attempting to send a test email to {0}".format(to))
    try:
        if ses_send_obj.send_email() == True:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        click.echo("unexpected exception")
        click.echo(e)
        sys.exit(1)



@click.command()
@click.option("--to", default="", help="Address you are sending to. Required")
@click.option("--fromaddr", default=None, help="The address you want the email to be from. Required")
@click.option("--awsregion", default=None, help="AWS region your SES service is hosted in. Required")
@click.option("--message_txt", default=None, help="Plain text version of your message body. Required")
@click.option("--message_html", default=None, help="html version of your message body. Optional")
@click.option("--subject", default=None, help="Email subject. Optional")
@click.option("--fromname", default=None, help="Name to list in from line. Optional")
def send_email(to, fromaddr, awsregion, message_txt, message_html, subject, fromname):
    if not to or to == "":
        click.echo("You need to provide an email address to send to.")
        sys.exit(1)
    if not fromaddr or fromaddr == "":
        click.echo("You need to provide a from address.")
        sys.exit(1)
    if not awsregion or awsregion == "":
        click.echo("You need to provide your AWS region.")
        sys.exit(1)
    if not message_txt or message_txt == "":
        click.echo("You need to provide an email message, at least in plain text.")
        sys.exit(1)

    try:
        # instantiate the object
        ses_send_obj = SESSender(sendto=to,fromaddr=fromaddr, aws_region=awsregion, message_txt=message_txt, message_html=message_html, msgsubject=subject, fromname=fromname)
    except Exception as e:
        click.echo("unexpected exception")
        click.echo(e)
        sys.exit(1)

    try:
        # validate the arguments and credentials
        check_validation = ses_send_obj.ses_validate()
        if check_validation == False:
            sys.exit(1)
    except Exception as e:
        click.echo("unexpected exception")
        click.echo(e)
        sys.exit(1)

    try:
        # if everything validated, try to send the email
        click.echo("Attempting to send an email to {0}".format(to))
        if ses_send_obj.send_email() == True:
            sys.exit(0)
        else:
            sys.exit(1)
    
    except Exception as e:
        click.echo("unexpected exception")
        click.echo(e)
        sys.exit(1)