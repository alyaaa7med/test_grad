from rest_framework import viewsets
from .models import Doctor , Patient 
from .serializers import DoctorSerializer , PatientSerializer 



class DoctorView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
