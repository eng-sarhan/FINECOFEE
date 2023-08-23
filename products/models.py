from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse


class Company(models.Model):
    comp = models.CharField(max_length=225)

    def __str__(self):
        return self.comp

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        ordering = ['-comp']


class Category(models.Model):
    categ = models.CharField(max_length=225)
    catParent = models.ForeignKey('self', limit_choices_to={'catParent__isnull': True}, on_delete=models.CASCADE,
                                  blank=True, null=True)

    def __str__(self):
        return self.categ

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ['-categ']


class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    price = models.FloatField()
    photo = models.ImageField(upload_to='photos/%y/%m/%d/')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField()
    categ = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    comp = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)

    slug = models.SlugField(blank=True, null=True, verbose_name=_("Product URL"))  # , verbose_name=_("Product URL")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-publish_date']
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})
