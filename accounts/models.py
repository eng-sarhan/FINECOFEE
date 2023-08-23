from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import datetime
from django_countries.fields import CountryField
# from django_countries import countries
# COUNTRY_DICT = dict(countries)
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from products.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE,)
    product_favorites = models.ManyToManyField(Product)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(_("image"), upload_to='profile_img', blank=True, null=True)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    # country = CountryField(blank_label="(select country)")
    # country = CountryField()
    # country = countries

    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    join_date = models.DateTimeField(_("join date"), default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return '%s' % self.user

    def get_absolute_url(self):
        return reverse("accounts:Profile", kwargs={"slug": self.slug})


def create_profile(sender, **kwargs):
    print(kwargs)
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
