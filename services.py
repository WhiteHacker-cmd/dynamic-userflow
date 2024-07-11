from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()
import smtplib
import jinja2


 # Load the Jinja2 template and render it
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
template = env.get_template("template/email.html")
html_message = template.render()



EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
to_addresses = ["shraddha@aviato.consulting", "pooja@aviato.consulting", "prijesh@aviato.consulting"]


async def send_email():
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(to_addresses)
    msg['Subject'] = "API Document Invitation"
    msg.attach(MIMEText(html_message, 'html'))


    part = MIMEBase('application', 'octet-stream')
    with open("example/db.png", 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename("example/db.png")}')
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_addresses, msg.as_string())
        server.close()
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

