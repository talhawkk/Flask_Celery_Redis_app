from celery_app import celery
import datetime,time
import pandas as pd
from reportlab.pdfgen import canvas
from smtplib import SMTP
from email_utils import send_email_smtp
# command to run celery worker (1), on windows:
# celery -A celery_app worker --loglevel=info --pool=solo
# command to run celery worker (2), on linux:
# celery -A celery_app worker --loglevel=info



@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def send_email(self, to, subject, body):
    try:
        time.sleep(5)  
        send_email_smtp(to, subject, body)
        return "Email has been sent successfully"
    except Exception as e:
        raise self.retry(exc=e)

@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def generate_report(self, report_type, data=None):
    try:
        time.sleep(10)  
        
        # Default data if user doesn't provide any
        default_data = {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [30, 25, 35],
            "City": ["New York", "Los Angeles", "Chicago"]
        }
        
        report_data = data if data else default_data
        
        if report_type == "csv":
            df = pd.DataFrame(report_data)
            df.to_csv(f"report_{self.request.id}.csv", index=False)
            return "CSV report generated successfully"
        elif report_type == "pdf":
            c = canvas.Canvas(f"report_{self.request.id}.pdf")
            c.drawString(100, 750, "PDF Report")
            
            # Get column names and data
            columns = list(report_data.keys())
            num_rows = len(list(report_data.values())[0])
            
            # Draw header
            y_position = 720
            header_text = " | ".join(columns)
            c.drawString(100, y_position, header_text)
            
            # Draw data rows
            for i in range(num_rows):
                y_position -= 20
                row_text = " | ".join(str(report_data[col][i]) for col in columns)
                c.drawString(100, y_position, row_text)
            
            c.save()
            return "PDF report generated successfully"
        else:
            return "Unsupported report type, please choose 'csv' or 'pdf'"
    except Exception as e:
        return str(e)