from io import BytesIO

from celery import shared_task
from django.template.loader import render_to_string

from webapp.models import NetworkNode
import random
import qrcode
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


@shared_task
def increase_debt():
    nodes = NetworkNode.objects.all()
    for node in nodes:
        node.debt += random.randint(5, 500)
    NetworkNode.objects.bulk_update(nodes, ['debt'])


@shared_task
def debt_reduction():
    nodes = NetworkNode.objects.all()
    for node in nodes:
        random_num = random.randint(100, 10000)
        node.debt -= random_num if random_num >= node.debt else 0
    NetworkNode.objects.bulk_update(nodes, ['debt'])


@shared_task(ignore_result=True, max_retries=3)
def make_debt_zero():
    NetworkNode.objects.update(debt=0)


@shared_task
def generate_qr_code_and_send_email(email, network_node_data):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        text_representation = '\n'.join([f'{key}: {value}' for key, value in network_node_data.items()])

        qr.add_data(text_representation)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        image_buffer = BytesIO()
        img.save(image_buffer)
        image_buffer.seek(0)

        subject = "QR Code for Network Node"
        html_message = render_to_string(
            'email/network_node_info.html',  # Adjust 'your_app_name' to your actual app name
            network_node_data
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        email_message = EmailMessage(subject, html_message, from_email, recipient_list)
        email_message.content_subtype = 'html'
        email_message.attach('qrcode.png', image_buffer.read(), 'image/png')
        email_message.send(fail_silently=False)
    except Exception as e:
        return False
    return True
