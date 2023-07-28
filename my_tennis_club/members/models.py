
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .emails import send_account_activation_email

class Profiles(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_verified = models.BooleanField(default=False,blank=True)
    email_token = models.CharField(max_length=200,null=True,blank=True)
    profile_image=models.ImageField(upload_to='profile')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    uuid = models.UUIDField( default='',null=False,blank=True, editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update uuid and ovoid clash with existing code '''
        if not self.uuid:
            self.uuid = uuid.uuid4()
        return super(Profiles, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            Profiles.objects.create(user=instance,email_token=email_token)
            email=instance.email
            send_account_activation_email(email, email_token)

    except Exception as e:
        print(e)
# Create your models here.
class Addresses(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")

    def __str__(self):
        return self.locality


class Categories(models.Model):
    STATUS = (('PUBLISH', 'PUBLISH'), ('DRAFT', 'DRAFT'))
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    status = models.CharField(choices=STATUS, max_length=160, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.category_image.url
        except:
            url = ''
        return url


class Colors(models.Model):
    title = models.CharField(max_length=50, verbose_name="Color Title")
    slug = models.SlugField(max_length=55, verbose_name="Color Slug")
    code = models.CharField(max_length=70,default='')
    productColor_count = models.CharField(max_length=50, verbose_name="productColor count")

    def __str__(self):
        return self.title
class Size(models.Model):
    title = models.CharField(max_length=50, verbose_name="Size Title")
    slug = models.SlugField(max_length=55, verbose_name="Size Slug")
    productSize = models.CharField(max_length=50, default='', verbose_name="productSize ")
    productSize_count = models.CharField(max_length=50, verbose_name="productSize count")

    def __str__(self):
        return self.productSize

class fabrics(models.Model):
    title = models.CharField(max_length=50, verbose_name="Fabric Title")
    slug = models.SlugField(max_length=55, verbose_name="Fabric Slug")
    fabric_count = models.CharField(max_length=50, verbose_name="Fabric count")

    def __str__(self):
        return self.title
class filter_price(models.Model):
    FILTER_PRICE=(
        ('1000 TO 10000','1000 TO 10000'),
        ('10000 TO 20000','10000 TO 20000'),
        ('20000 TO 30000','20000 TO 30000'),

    )

    price = models.CharField( choices=FILTER_PRICE,max_length=50, verbose_name="filter_price ")

    def __str__(self):
        return self.price

class Products(models.Model):
    CONDITION=(('NEW','NEW'),('OLD','OLD'))
    STOCK = (('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK'))
    STATUS = (('PUBLISH', 'PUBLISH'), ('DRAFT', 'DRAFT'))
    unique_id= models.CharField( unique=True, null=True,blank=True,max_length=150)
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    size = models.ForeignKey(Size, default=True, verbose_name="Product size", on_delete=models.CASCADE)
    color = models.ForeignKey(Colors, default=True, verbose_name="Product Color", on_delete=models.CASCADE)
    fabric = models.ForeignKey(fabrics,default=True, verbose_name="Product Fabric", on_delete=models.CASCADE)
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='products', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    filter_price = models.ForeignKey(filter_price, default=True,  on_delete=models.CASCADE)
    condition = models.CharField(choices=CONDITION,max_length=150,default='')
    stock = models.CharField( choices=STOCK, max_length=150,default='')
    status=models.CharField(choices=STATUS,max_length=160,default='')
    category = models.ForeignKey(Categories, verbose_name="Product Categoy", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    def save(self):
        if self.unique_id is None and self.created_at and self.id:
            self.unique_id=str(self.created_at) +str(self.id)
        return super().save()

    @property
    def imageURL(self):
        try:
            url=self.product_image.url
        except:
            url=''
        return url


class productAttribute(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/img', blank=True, null=True)
    product = models.ForeignKey(Products,  on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name_plural='7. productAttribute'

    def __str__(self):
        return self.product.title



class images(models.Model):
    image = models.ImageField(upload_to='products/img', blank=True, null=True)
    product = models.ForeignKey(Products,  on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=150)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)

    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Addresses, verbose_name="Shipping Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
    )

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True)
