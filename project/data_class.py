import csv
import os
from utils.templates import get_template, render_context
import datetime
from smtplib import SMTP, SMTPException, SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.rw_csv import edit_data

host = 'smtp.gmail.com'
port = 587
username = 'yourGmail@gmail.com'
password = 'yourPassword'
file_item_path = os.path.join(os.getcwd(), 'data.csv')


class UserManager:

    def render_message(self, user_data):
        file_ = 'templates\email_message.txt'
        file_html = 'templates\email_message.html'
        template = get_template(file_)
        template_html = get_template(file_html)
        if isinstance(user_data, dict):
            plain_ = render_context(template, user_data)
            html_ = render_context(template_html, user_data)
            return plain_, html_
        return None, None

    def message_user(self, user_id=None, email=None, subject='Billing Update!'):
        user = self.get_user_data(user_id=user_id, email=email)
        if user:
            if self.send_email(user, subject):
                print('Message was sent successfully to {name}'.format(name=user["name"]))
                edit_data(edit_id=user_id, email=email, amount=user.get('amount', 0), sent=True)

        return False

    def send_email(self, user, subject):
        plain_, html_ = self.render_message(user)
        email_con = SMTP(host, port)
        email_con.ehlo()
        email_con.starttls()
        try:
            user_email = user.get('email', username)
            email_con.login(username, password)
            the_msg = MIMEMultipart('alternative')
            the_msg['Subject'] = subject
            the_msg['From'] = username
            the_msg['To'] = user_email
            plain_txt = MIMEText(plain_, 'plain')
            html_txt = MIMEText(html_, 'html')
            the_msg.attach(plain_txt)
            the_msg.attach(html_txt)
            email_con.sendmail(username, [user_email], the_msg.as_string())
            email_con.quit()
        except SMTPAuthenticationError:
            print('Could not login')
            return False
        except SMTPException:
            print('error sending message')
            return False
        return True

    def get_user_data(self, user_id=None, email=None):
        with open(file_item_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            unknown_user_id = None
            unknown_email = None
            for row in reader:
                if user_id is not None:
                    if int(user_id) == int(row.get('id')):
                        return row
                    else:
                        unknown_user_id = user_id
                if email is not None:
                    if email == row.get('email'):
                        return row
                    else:
                        unknown_email = email
            if unknown_user_id is not None:
                print('User id {user_id} not found'.format(user_id=user_id))
            if unknown_email is not None:
                print('Email {email} not found'.format(email=email))
        return None

