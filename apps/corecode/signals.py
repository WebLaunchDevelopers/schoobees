from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from datetime import datetime

from .models import AcademicSession, AcademicTerm

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
