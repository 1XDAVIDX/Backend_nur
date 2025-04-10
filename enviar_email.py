# enviar_email.py
import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def enviar_email(destinatario: str, asunto: str, mensaje: str):
    email_sender = os.getenv("EMAIL_SENDER")
    PASSWORDEMAIL = os.getenv("PASSWORDEMAIL")

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = destinatario
    em["Subject"] = asunto
    em.set_content(mensaje)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, PASSWORDEMAIL)
            smtp.sendmail(email_sender, destinatario, em.as_string())
        return {"mensaje": "Correo enviado exitosamente"}
    except Exception as e:
        return {"error": str(e)}
