import smtplib
import logging
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class Emailer(object):

    def __init__(self):
        self.sender = 'msantdev@gmail.com'
        self.recipients = ['matteosantama@gmail.com']
        self.username = 'msantdev'
        self.psswd = 'whtrad1ng'
        self.logger = logging.getLogger(__name__)


    def send_mail(self, subject, body):
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(self.username, self.psswd)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.recipients)

        self.logger.info('Sending email with subject %s', subject)

        server_ssl.sendmail(self.sender, self.recipients, msg.as_string())
        server_ssl.close()
