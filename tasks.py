import os
import smtplib
import logging
from celery import Celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Celery
celery = Celery(
    'tasks',
    broker=os.getenv('CELERY_BROKER_URL'),
    backend=os.getenv('CELERY_RESULT_BACKEND')
)

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))

# Configure logging
logging.basicConfig(level=logging.INFO)

@celery.task(bind=True)
def send_email(self, email):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = email
        msg['Subject'] = "Subject: Test"
        body = "I did it y'all. Python app with celery and rabbitmq configured"
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(EMAIL, email, msg.as_string())
        server.quit()

        logging.info(f'Email sent to {email}')
        print("Email sent")
        return f"Email sent successfully to {email}"
    except Exception as e:
        logging.error(f'Failed to send email to {email}: {e}')
        print("Email not sent")
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise # This will mrk as test failed
