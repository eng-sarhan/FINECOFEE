from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import datetime
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from products.models import Product
from creditcards.models import CardNumberField,CardExpiryField,SecurityCodeField


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    order_date = models.DateTimeField(_("order date"), default=datetime.datetime.now)
    details=models.ManyToManyField(Product, through='OrderDetails')
    is_finished=models.BooleanField()
    total = 0
    items_count = 0


    def __str__(self):
        return 'User: ' + self.user.username +',Order id: '+ str(self.id)


class OrderDetails(models.Model):
    product=models.ForeignKey(Product,on_delete = models.CASCADE)
    order=models.ForeignKey(Order,on_delete = models.CASCADE)
    price=models.FloatField()
    quantity=models.IntegerField()

    def __str__(self):
        return 'User: ' + self.order.user.username +',Product: '+ self.product.name +',Order id: '+ str(self.order.id)

    class Meta:
        ordering = ['-id']


class Payment(models.Model):
    order=models.ForeignKey(Order,on_delete = models.CASCADE)
    ship_address=models.CharField(max_length = 150)
    ship_phone=models.CharField(max_length = 50)
    card_number=CardNumberField()
    expire=CardExpiryField()
    security_code=SecurityCodeField()


