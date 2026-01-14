from celery_app import celery
import datetime,time
import pandas as pd
from reportlab.pdfgen import canvas
from smtplib import SMTP
from email_utils import send_email_smtp
# command to run celery worker:
# celery -A celery_app worker --loglevel=info --pool=solo


@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def send_email(self, to, subject, body):
    try:
        send_email_smtp(to, subject, body)
        return "Email has been sent successfully"
    except Exception as e:
        raise self.retry(exc=e)

@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def generate_report(self, report_type):
    try:
        time.sleep(50)  # Simulate report generation delay
        if report_type == "csv":
            df=pd.DataFrame({
                "Name":["Alice","Bob","Charlie"],
                "Age":[30,25,35],
                "City":["New York","Los Angeles","Chicago"]
            })
            df.to_csv(f"report_{self.request.id}.csv", index=False)
            return "CSV report generated successfully"
        elif report_type == "pdf":
            c=canvas.Canvas(f"report_{self.request.id}.pdf")
            c.drawString(100,750,"Sample PDF Report generated")
            c.drawString(100,730,"Generated using ReportLab")
            c.save()
            return "PDF report generated successfully"
        else:
            return "Unsupported report type, please choose 'csv' or 'pdf'"
    except Exception as e:
        return str(e)