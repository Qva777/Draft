from django.db import models
from E_Shop_API.E_Shop_Products.validators import validate_negative


class Product(models.Model):
    """  Product models/fields  """
    name = models.CharField(verbose_name='Name', unique=True, max_length=64, blank=False, )
    description = models.CharField(verbose_name='Description', max_length=255, blank=True)

    photo = models.ImageField(verbose_name='Photo', upload_to='photos', max_length=255, blank=True)
    price = models.FloatField(verbose_name='Price', validators=[validate_negative], max_length=100000, blank=False)
    count = models.IntegerField(verbose_name='Count', validators=[validate_negative], blank=False)

    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        """ String representation """
        return self.name

    class Meta:
        """ Representation in admin panel """
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
