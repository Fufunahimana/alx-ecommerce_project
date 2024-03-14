from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = [
    ('DZ', 'Algeria'),
    ('AO', 'Angola'),
    ('BJ', 'Benin'),
    ('BW', 'Botswana'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('CM', 'Cameroon'),
    ('CV', 'Cape Verde'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Congo, Democratic Republic of the'),
    ('DJ', 'Djibouti'),
    ('EG', 'Egypt'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('ET', 'Ethiopia'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GH', 'Ghana'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('CI', 'Ivory Coast'),
    ('KE', 'Kenya'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('ML', 'Mali'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('NA', 'Namibia'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('RW', 'Rwanda'),
    ('ST', 'São Tomé and Príncipe'),
    ('SN', 'Senegal'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('SS', 'South Sudan'),
    ('SD', 'Sudan'),
    ('SZ', 'Swaziland'),
    ('TZ', 'Tanzania'),
    ('TG', 'Togo'),
    ('TN', 'Tunisia'),
    ('UG', 'Uganda'),
    ('EH', 'Western Sahara'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe'),
]

CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lass'),
    ('MS','Milkshake'),
    ('PN','Panner'),
    ('GH','Ghee'),
    ('CZ','Cheeze'),
    ('IC','Ice-Cream'),
    ('KF','KUFFI'),
)

class Product(models.Model):
    title = models.CharField(max_length =100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices =CATEGORY_CHOICES,max_length =2)
    product_image = models.ImageField(upload_to='product')    
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models. IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    
    def __str__(self):
        return self.name 