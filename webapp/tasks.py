from celery import shared_task

from webapp.models import NetworkNode
import random


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
