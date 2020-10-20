"""Application module to manage email communication."""

# Standard imports
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# Application imports
from obya import Config
from obya import log


def send(body, subject, attachments=None):
    """Read a configuration file.

    Args:
        body: Text for email body
        subject: Subject for email
        attachments: List of filepaths to attach

    Returns:
        success: True if succesful

    """
    # Initialize key variables
    success = False
    config = Config()

    # Create SMTP TLS session
    client = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        client.ehlo()
    except:
        _exception = sys.exc_info()
        log_message = 'Gmail Communication Failure'
        log.log2exception(1013, _exception, message=log_message)
    client.starttls()

    # Authentication
    try:
        client.login(config.smtp_user, config.smtp_pass)
    except:
        _exception = sys.exc_info()
        log_message = 'Gmail Authentication Failure'
        log.log2exception(1014, _exception, message=log_message)
        return success

    # Format message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = config.email_from
    message['To'] = ', '.join(config.email_to)
    message.add_header('reply-to', config.email_from)
    html = '''
<html>
    <head></head>
    <body><font face="courier">
        {}
    </font></body>
</html>
'''.format('<br>'.join('&nbsp;'.join(body.split(' ')).split('\n')))

    message.attach(MIMEText(html, 'html', 'UTF-8'))

    # Add attachment if required
    if bool(attachments) is True:
        if isinstance(attachments, list) is True:
            for attachment in attachments:
                part = MIMEApplication(open(attachment, 'rb').read())
                part.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=('{}'.format(attachment)))
                message.attach(part)

    # Send
    try:
        client.sendmail(
            config.email_from, config.email_to, message.as_string())
        success = True
    except:
        _exception = sys.exc_info()
        log_message = 'Gmail Send Failure'
        log.log2exception(1015, _exception, message=log_message)
        return success
    finally:
        client.quit()
    return success
