from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.db.models.fields.related import ForeignKey  
# Create your models here.

class LoginDetail(models.Model):
	LoginID   = models.ForeignKey(User, on_delete=models.CASCADE)
	Username  = models.CharField(max_length=30)
	Email     = models.CharField(max_length=50)
	LoginTime = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name  = models.CharField(max_length=100) 
    price = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='images/')

class Offers(models.Model):
   OfferName    = models.CharField(max_length=30,unique=True)
   OfferPrice   = models.DecimalField(max_digits=8, decimal_places=2) 
   Availability = models.CharField(max_length=10,blank=True)
   CreateTime   = models.DateTimeField(auto_now=True)
   def __str__(self):
      return str(self.id)

class Employee(models.Model):
   FirstName     = models.CharField(max_length=30)
   LastName      = models.CharField(max_length=30,blank=True)
   CNIC          = models.CharField(max_length=13,unique=True,blank=True)
   FatherName    = models.CharField(max_length=30)
   Age           = models.IntegerField()
   Gender        = models.CharField(max_length=8)
   MaritalStatus = models.CharField(max_length=10)
   EntryDate     = models.DateTimeField(auto_now=True)
   def __str__(self):
      return str(self.id)

class Delivery(models.Model):
   EmployeePID     = models.ForeignKey(Employee,on_delete=models.CASCADE)
   CustomerOrderID = models.ForeignKey(User, on_delete=models.CASCADE) 
   DeliveryAddress = models.CharField(max_length=100)
   ExpectedTime    = models.CharField(max_length=10)
   EntryDate       = models.DateTimeField(auto_now=True)
   def __str__(self):
      return str(self.id)

class contactus(models.Model):
   Name      = models.CharField(max_length=30)
   Email     = models.CharField(max_length=50)
   Message   = models.CharField(max_length=250)
   EntryDate = models.DateTimeField(auto_now=True)
   def __str__(self):
      return str(self.id)

class WebResources(models.Model):
   Location  = models.CharField(max_length=250,blank=True)
   Phone = models.CharField(max_length=13,unique=True,blank=True)
   Day   = models.CharField(max_length=10,blank=True)
   OpeningTime = models.TimeField(blank=True)
   ClosingTime = models.TimeField(blank=True)
   LinkedInLink = models.CharField(max_length=100,blank=True)
   GitLink = models.CharField(max_length=100,blank=True)
   TwitterLink = models.CharField(max_length=100,blank=True)
   FbLink = models.CharField(max_length=100,blank=True)
   EntryDate = models.DateTimeField(auto_now=True)
   def __str__(self):
      return str(self.id)
class CEO(models.Model):
   Image     = models.ImageField(upload_to="images/")
   Name      = models.CharField(max_length=30)
   Rank      = models.CharField(max_length=50)
   EntryDate = models.DateTimeField(auto_now=True)
   def __str__(self):
      return str(self.id)

#------cart-------------------
class Req_info(models.Model):
    status=models.CharField(max_length=255, default='Pending')
    Name_Costomer=models.CharField(max_length=255, null=True)
    GrandTotal=models.FloatField(  null=True,default='0.00' )
    Address = models.CharField(max_length=255,null=True)
    Phone = models.CharField(max_length=15,null=True)
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
      return str(self.id)

class OrdereProduct(models.Model):
    order = models.ForeignKey(Req_info, on_delete=models.CASCADE)
    CustomerID = models.IntegerField(null=True)
    Name_Costomer=models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity= models.FloatField()
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
      return str(self.order)
#--------endcart---------------