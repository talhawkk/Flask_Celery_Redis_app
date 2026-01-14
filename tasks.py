from celery_app import celery
import datetime,time
import pandas as pd
from reportlab.pdfgen import canvas


@celery.task(bind=True, max_retries=3, default_retry_delay=7)
def send_email(self, to, subject, body):
    try:
        time.sleep(5)  # Simulate email sending delay
        print(f"Email sent to {to} with subject '{subject}'")
        return "email has been sent successfully"
    except Exception as e:
        raise self.retry(exc=e)
    

@celery.task(bind=True)
def generate_report(self, report_type):
    try:
        if report_type == "csv":
            df=pd.DataFrame({
                "Name":["Alice","Bob","Charlie"],
                "Age":[30,25,35],
                "City":["New York","Los Angeles","Chicago"]
            })
            df.to_csv("report.csv", index=False)
            return "CSV report generated successfully"
        elif report_type == "pdf":
            c=canvas.Canvas("report.pdf")
            c.drawString(100,750,"Sample PDF Report generated")
            c.drawString(100,730,"Generated using ReportLab")
            c.save()
            return "PDF report generated successfully"
        else:
            return "Unsupported report type, please choose 'csv' or 'pdf'"
    except Exception as e:
        return str(e)