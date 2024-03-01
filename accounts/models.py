from django.db import models
from django.contrib.auth.models import AbstractBaseUser  ,PermissionsMixin 
from django.utils.translation import gettext_lazy as _ 
from .managers import CustomUserManger 
import secrets 

class User(AbstractBaseUser,PermissionsMixin) :
    #Limit the values the 1st is the actual will stored in the database , but the 2nd is the readable in the admin 
    ROLE_CHOICES =[
        ('doctor','Doctor'),
        ('patient','Patient'),
        ('guest','Guest')
    ] 
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=90)
    email=models.EmailField(max_length=250,unique=True)
    password = models.CharField(max_length= 15)
    is_staff = models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)  
    role =models.CharField(max_length = 10, choices = ROLE_CHOICES ,default='guest' )


    USERNAME_FIELD= "email"
    REQUIRED_FIELDS= ["first_name","last_name"]  # required fields you need to create an account

    objects = CustomUserManger()

    # class Meta : 
    #     verbose_name = _("User")
    #     verbose_name_plural = _("Users")

    def __str__(self) :
        return self.email
    
    # @property 
    # def get_full_name(self):
    #     return f"{self.first_name} {self.last_name}"
    

class otpcode(models.Model): 
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    otp=models.CharField(max_length=6, default = secrets.token_hex(3)[:5])
    otp_created_at = models.DateTimeField(auto_now_add = True )
    otp_expired_at = models.DateTimeField(blank= True , null = True) # why ? 




# not all relations have been added ^_^    
class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone= models.CharField(max_length=15,null=True)
    syndicateNo = models.CharField(max_length=15, blank=False , null = False)
    university = models.CharField(max_length=30)
    specialization = models.CharField(max_length=255)
    gender= models.CharField(max_length=7,default='unknown')


class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender= models.CharField(max_length=7,default='unknown')
    birthdate = models.DateField()



# request_counter_signal = Signal(providing_args['timestamp'])

# def func(request) :
#     request_counter_signal.send(sender = Post,timestamp='2010-10-1')
#     return HttpResponse("it is response")

# @reciever(request_counter_signal)
# def post_counter_signal(sender,**kwargs) :
#     print (kwargs)