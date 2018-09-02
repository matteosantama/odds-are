import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Emailer(object):


    def __init__(self):
        self.sender = 'sender@address.com'
        self.recipients = ['list@recipients.com']
        self.username = 'gmail_username'
        self.psswd = 'gmail_psswd'


    def send_opps(self, body):
        self.server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server_ssl.ehlo()
        self.server_ssl.login(self.username, self.psswd)

        subject = 'Sure Profit Opportunities'

        text = """
                From: %s
                To: %s
                Subject: %s

                %s
                """ % (self.sender, ', '.join(self.recipients), subject, body)

        server.sendmail(self.sender, self.recipients, text)
        server.close()
