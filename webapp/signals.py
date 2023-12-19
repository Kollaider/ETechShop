from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from webapp.models import EmployeeProfileInfo


@receiver(post_save, sender=User)
def create_or_update_employee_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfileInfo.objects.create(user=instance)
    else:
        instance.employeeprofileinfo.save()
