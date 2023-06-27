"""
Helper methods for email sending functionality
"""

import logging
import smtplib
import email.utils
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template import Template
from django.template import loader
from decouple import config

LOGGER = logging.getLogger(__name__)


class EmailHelper:
    """
    email class
    """

    @staticmethod
    def send_email(recipient, subject, body, pdf_file, file_name, bcc=None):
        """
        send mail as per recipient list
        """
        msg = MIMEMultipart('alternative')
        part1 = MIMEText(body, 'html')
        msg.attach(part1)
        if pdf_file and file_name:
            attach = MIMEApplication(pdf_file, _subtype="pdf")
            attach.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(attach)
        msg['Subject'] = subject
        msg['From'] = email.utils.formataddr((config('sender_name'), config('sender')))  # sender_name, sender
        msg['To'] = recipient
        msg['Bcc'] = bcc
        if bcc:
            recipients = [recipient] + [bcc]
        else:
            recipients = recipient
        try:
            server = smtplib.SMTP(config('host'), config('port'))
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(config('smtp_username'), config('smtp_password'))
            server.sendmail(config('sender'), recipients, msg.as_string())
            server.close()

        except smtplib.SMTPAuthenticationError as sm_err:
            LOGGER.error(sm_err)
        except smtplib.SMTPConnectError as con_err:
            LOGGER.error(con_err)
        except smtplib.SMTPNotSupportedError as se_err:
            LOGGER.error(se_err)
        except smtplib.SMTPDataError as dt_err:
            LOGGER.error(dt_err)
        except Exception as ex_err:
            LOGGER.error("Error: %s", ex_err)

    def send_notification(self, post_set, template_name, subject, recipient, pdf_file=None, file_name=None, bcc=None):
        """
        mail send details
        """
        email_subject = subject
        LOGGER.debug("Email subject: %s", email_subject)
        email_body = post_set
        if template_name:
            template = loader.get_template(template_name)
        else:
            template = Template(email_body)
        context = post_set
        body_text = template.render(context)
        self.send_email(recipient=recipient,
                        subject=email_subject,
                        body=body_text,
                        pdf_file=pdf_file,
                        file_name=file_name,
                        bcc=bcc)
