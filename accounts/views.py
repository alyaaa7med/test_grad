from rest_framework import viewsets
from .models import Doctor , Patient 
from .serializers import DoctorSerializer , PatientSerializer,VerifyOTPSerializer , EmailSerializr
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User  ,otpcode 
from django.utils import timezone
import secrets
from django.core.mail import send_mail



class DoctorView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer



@api_view(['POST'])
def generate_otp_from_email_and_send_email(request):

    if request.method == 'POST':
        serializer = EmailSerializr(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=404)
            
            otp = otpcode.objects.create(user=user, otp=secrets.token_hex(3)[:5]) #  Fields that have default values or are nullable (blank=True, null=True) can be omitted if you're satisfied with the defaults or if they can be left empty.
            otp.otp_expired_at = timezone.now() + timezone.timedelta(minutes=5)  # Set OTP expiration time
            otp.save()

            subject="Email Code"
            message = f""" here is your OTP {otp.otp} 
                           it expires in 5 minutes 
                                 """
            sender = "alyaa_ahmed@gmail.com"
            receiver = [user.email, ]
       
            # send email
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
               )
  
               
            return Response({'message': 'OTP created and Email received successfully'}, status=201)
    
  


@api_view(['POST','PUT'])

# pk of user , foreign key in otp , doctor , patient model 
def verify_code_and_resend(request,pk):
    
    #check the user 
    user = get_object_or_404(User, pk=pk)
    try:
        otp_instance = otpcode.objects.get(user=user)
    except otpcode.DoesNotExist:
        return Response({'message': 'OTP code not found for this user'}, status=404)
    
    # verify otp code for the user 
    if request.method == 'POST':
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():            
            # check if it can be valid ?
            if otp_instance.otp == serializer.validated_data['otp_code']:
                # check if the otp is expired 
                if otp_instance.otp_expired_at > timezone.now():
                    return Response({'message': 'OTP is valid ,Go to Reset Password Page'}, status=200)
            
                # expired token
                return Response({'message': 'OTP is Expired , Resend it '}, status=400) #bad request
        
            # invalid otp code
            return Response({'message': 'Invalid OTP entered, enter a valid OTP! '}, status=400)
    

    # resend otp code for the user 
    if request.method == 'PUT' :

        otp_instance.otp = secrets.token_hex(3)[:5] 
        otp_instance.otp_created_at = timezone.now() 
        otp_instance.otp_expired_at = timezone.now() + timezone.timedelta(minutes=5)  # Set OTP expiration time

        # Save the updated otp_instance
        otp_instance.save()

        subject="Email Code"
        message = f""" here is your new OTP { otp_instance.otp} 
                           it expires in 5 minutes 
                                 """
        sender = "alyaa_ahmed@gmail.com"
        receiver = [user.email, ]
       
        # send email
        send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
  
            # Process the email as needed
        return Response({'message': 'New OTP created and Email received successfully'}, status=200)







# user.is_active=True # in the model it is false as default but to activate it send code as the man did in his code 
#                 user.save()