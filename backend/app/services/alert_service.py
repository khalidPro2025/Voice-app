# app/services/alert_service.py

import smtplib
from email.mime.text import MIMEText

ALERT_THRESHOLD_MM = 30  # seuil d’inondation

def check_and_alert(device_id: str, zone: str, niveau_mm: float):
    """
    Vérifie le niveau d’inondation et envoie une alerte si > seuil.
    """

    if niveau_mm < ALERT_THRESHOLD_MM:
        return False

    msg = f"""
    🚨 ALERTE INONDATION 🚨

    Capteur : {device_id}
    Zone : {zone}
    Niveau détecté : {niveau_mm} mm

    Action recommandée : Intervention d'urgence.
    """

    send_email_alert("Alertes CleanSen360 <noreply@cleansen360.sn>", 
                     "mairie@dakar.sn",
                     "Alerte Inondation - CleanSen360",
                     msg)

    print("Alerte envoyée.")
    return True


def send_email_alert(sender, recipient, subject, body):
    """
    Envoi d'un email d’alerte (SMTP local ou Gmail)
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP("mail:587") as server:
            server.sendmail(sender, recipient, msg.as_string())
        print("Email envoyé")
    except Exception as e:
        print("Erreur envoi email:", e)
