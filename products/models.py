import uuid
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_delete

class Category(models.Model):
    catergoy_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    name = models.CharField(_("Category Title"), max_length=255, unique=True, db_index=True, help_text=_("Required and unique"))
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    #def get_absolute_url(self):
    #    return reverse("products:category_list", args=[self.catergoy_uuid])

    def __str__(self):
        return self.name

class Size(models.TextChoices):
    XXS = 'xxs'
    XS = 'xs'
    S = 's'
    M = 'm'
    L = 'l'
    XL = 'xl'
    XXL = 'xxl'

class Collections(models.TextChoices):
    ACCSSORIES = 'Accssories'
    WOMEN = 'Womens'
    MENS = 'Mens'
    KIDS = 'Kids'

class ProductType(models.Model):
    name = models.CharField(_("Product Type"), max_length=255, help_text=_("Required"), unique = True)
    slug = models.SlugField(verbose_name=_("Product Type safe URL"), max_length=255, unique = True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    product_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(_("Product name"), max_length=255, help_text=_("Required"))
    size = models.CharField(_("Size"), max_length=10, choices=Size.choices)
    collection = models.CharField(_("Collection"), max_length=10, choices=Collections.choices)
    default_img = models.ImageField(upload_to="images/", default="images/default.png",)
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    price = models.DecimalField(
        verbose_name=_("Price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(get_user_model(), related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_average_review_score(self):
        average_score = 0.0
        if self.reviews.count() > 0:
            total_score = sum([review.rating for review in self.reviews.all()])
            average_score = total_score / self.reviews.count()
        return round(average_score, 1)

    # def get_absolute_url(self):
    #     return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(""), on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    author = models.CharField(max_length=50)
        
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

@receiver(pre_delete, sender=ProductImage)
def delete_shot_files_hook(sender, instance, using, **kwargs):
    instance.image.delete()

@receiver(pre_delete, sender=Product)
def delete_shot_files_hook(sender, instance, using, **kwargs):
    instance.default_img.delete()