import uuid
from django.db import models
from django.urls import reverse
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    user_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    photo = models.ImageField(_("Profile Photo"), upload_to="images/profile/")
    phone_number = models.CharField(_("Mobile number"), max_length=20, blank=True, unique=True)
    address1 = models.CharField(_("Address Line 1"), max_length=250, blank=True)
    address2 = models.CharField(_("Address Line 2"), max_length=250, blank=True)
    postal_code = models.CharField(_("Postcode"), max_length=20, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)

    def send_email(self):
        pass

    def get_absolute_url(self):
        # return reverse("model_detail", kwargs={"pk": self.pk})
        pass
    
# Signals for deleting object file from memory disk
@receiver(pre_delete, sender=Customer)
def delete_content_files_hook(sender, instance, using, **kwargs):
	instance.photo.delete()