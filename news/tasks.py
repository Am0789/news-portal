from celery import shared_task
from django.core.mail import send_mail


@shared_task
def news_sender(subject, message, from_email, recipients):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipients,
        fail_silently=False
    )
