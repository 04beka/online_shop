from django.urls import path
from .views import GenerateVerificationCodeView, ValidateVerificationCodeView

urlpatterns = [
    path('payment/generate-code/', GenerateVerificationCodeView.as_view(), name='generate-code'),
    path('payment/validate-code/', ValidateVerificationCodeView.as_view(), name='validate-code'),
]
