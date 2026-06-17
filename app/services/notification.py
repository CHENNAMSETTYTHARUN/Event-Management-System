import logging
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_welcome_email(email: str, full_name: str):
        logger.info(f"[EMAIL MOCK] To: {email} | Subject: Welcome to Event Management System!")
        logger.info(f"[EMAIL MOCK] Body: Hello {full_name}, thank you for registering with us.")

    @staticmethod
    def send_registration_confirmation_email(email: str, full_name: str, event_name: str):
        logger.info(f"[EMAIL MOCK] To: {email} | Subject: Registration Confirmed: {event_name}")
        logger.info(f"[EMAIL MOCK] Body: Hello {full_name}, your registration for the event '{event_name}' is confirmed.")

    @staticmethod
    def send_ticket_email(email: str, full_name: str, event_name: str, ticket_number: str):
        logger.info(f"[EMAIL MOCK] To: {email} | Subject: Your Ticket for {event_name}")
        logger.info(f"[EMAIL MOCK] Body: Hello {full_name}, your ticket (Number: {ticket_number}) for '{event_name}' has been successfully generated. QR Code is attached.")

    def trigger_welcome_email(self, background_tasks: BackgroundTasks, email: str, full_name: str):
        background_tasks.add_task(self.send_welcome_email, email, full_name)

    def trigger_registration_confirmation(self, background_tasks: BackgroundTasks, email: str, full_name: str, event_name: str):
        background_tasks.add_task(self.send_registration_confirmation_email, email, full_name, event_name)

    def trigger_ticket_email(self, background_tasks: BackgroundTasks, email: str, full_name: str, event_name: str, ticket_number: str):
        background_tasks.add_task(self.send_ticket_email, email, full_name, event_name, ticket_number)

notification_service = NotificationService()
