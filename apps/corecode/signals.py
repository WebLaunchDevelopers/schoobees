from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from datetime import datetime

from .models import AcademicSession, AcademicTerm

# @receiver(post_migrate)
# def create_default_academic_session(sender, **kwargs):
#     def get_academic_year():
#         current_year = datetime.now().year
#         if datetime.now().month < 8:
#             # If current month is less than August, then academic year is previous year - current year
#             return f"{current_year - 1}-{current_year}"
#         else:
#             # If current month is greater than or equal to August, then academic year is current year - next year
#             return f"{current_year}-{current_year + 1}"
#     default_name = get_academic_year()
#     if not AcademicSession.objects.exists():
#         AcademicSession.objects.create(name=default_name, current=True)

# @receiver(post_migrate)
# def create_default_academic_term(sender, **kwargs):
#     if not AcademicTerm.objects.exists():
#         AcademicTerm.objects.create(name='1st Term', current=True)

@receiver(post_save, sender=AcademicSession)
def after_saving_session(sender, created, instance, *args, **kwargs):
    """Set current to False for other AcademicSession of the same user"""
    if instance.current is True and instance.pk:
        AcademicSession.objects.filter(user=instance.user).exclude(pk=instance.pk).update(current=False)


@receiver(post_save, sender=AcademicTerm)
def after_saving_term(sender, created, instance, **kwargs):
    """Set current to False for other AcademicTerms of the same user"""
    if instance.current is True and instance.pk:
        AcademicTerm.objects.filter(user=instance.user).exclude(pk=instance.pk).update(current=False)

