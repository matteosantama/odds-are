import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate


class Emailer(object):

    def __init__(self):
        self.developer = 'msantdev@gmail.com'
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
        msg['From'] = self.developer
        msg['To'] = ', '.join(self.recipients)

        self.logger.info('Sending email with subject %s', subject)

        server_ssl.sendmail(self.developer, self.recipients, msg.as_string())
        server_ssl.close()


    def send_log(self, file_name):
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(self.username, self.psswd)

        msg = MIMEMultipart()
        msg['From'] = self.developer
        msg['To'] = self.developer
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'App Logs'

        text = 'Find the logs for odds-are attached'
        msg.attach(MIMEText(text))

        part = MIMEBase('application', 'octet-stream')
        with open('./output.log', 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(file_name))
        msg.attach(part)

        self.logger.info('Sending log email')

        server_ssl.sendmail(self.developer, self.developer, msg.as_string())
        server_ssl.close()
