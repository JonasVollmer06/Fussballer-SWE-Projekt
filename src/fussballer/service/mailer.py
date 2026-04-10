"""Klasse für den MailService."""

from email.mime.text import MIMEText
from email.utils import make_msgid
from smtplib import SMTP, SMTPServerDisconnected
from socket import gaierror
from typing import Final
from uuid import uuid4

from loguru import logger

from fussballer.config import mail_enabled, mail_host, mail_port, mail_timeout
from fussballer.service.fussballer_dto import FussballerDTO

__all__ = ["send_mail"]

MAILSERVER: Final = mail_host
PORT: Final = mail_port
SENDER: Final = "Python Server <python.server@acme.com>"
RECEIVERS: Final = ["Buchhaltung <buchhaltung@acme.com>"]
TIMEOUT: Final = mail_timeout


def send_mail(fussballer_dto: FussballerDTO) -> None:
    """Funktion zum Senden von Mails."""
    if not mail_enabled:
        return

    msg: Final = MIMEText(f"Neuer Fussballer: <b>{fussballer_dto.nachname}</b>")
    msg["Subject"] = f"Neuer Fussballer: ID={fussballer_dto.id}"
    msg["Message-ID"] = make_msgid(idstring=str(uuid4()))

    try:
        with SMTP(host=MAILSERVER, port=PORT, timeout=TIMEOUT) as smtp:
            smtp.sendmail(from_addr=SENDER, to_addrs=RECEIVERS, msg=msg.as_string())
    except ConnectionRefusedError:
        logger.warning("ConnectionRefusedError")
    except SMTPServerDisconnected:
        logger.warning("SMTPServerDisconnected")
    except gaierror:
        logger.warning("socket.gaierror: Laeuft der Mailserver im virtuellen Netzwerk?")
