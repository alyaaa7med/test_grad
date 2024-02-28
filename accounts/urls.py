
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import DoctorView , PatientView 

router = DefaultRouter()
router.register(r'Doctor', DoctorView)
router.register(r'Patient',PatientView)


urlpatterns = [
    path('auth/',include('djoser.urls')),
    #for jwt
    path('auth/',include('djoser.urls.jwt')),
    path('apis/token/',TokenObtainPairView.as_view()),
    path('api/refreshtoken/',TokenRefreshView.as_view()),
    path('', include(router.urls)),

]