from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Verification

@receiver(post_save, sender=Verification)
def handle_verification_status_change(sender, instance, **kwargs):

    if instance.status == 'approved' and not instance.reviewed_at:
        instance.approve()
    elif instance.status == 'rejected' and not instance.reviewed_at:
        instance.reject()
