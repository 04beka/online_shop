import random
from django.core.cache import cache
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

CODE_EXPIRATION_SECONDS = 3600  # 1 საათი


class GenerateVerificationCodeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        key = f"payment_code_{user.id}"
        code = str(random.randint(1000, 9999))


        cache.set(key, code, timeout=CODE_EXPIRATION_SECONDS)

        return Response({
            'code': code,
            'message': f'4-digit code generated for {user.email} and is valid for 1 hour.'
        }, status=status.HTTP_200_OK)


class ValidateVerificationCodeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        submitted_code = request.data.get('code')
        key = f"payment_code_{user.id}"

        stored_code = cache.get(key)

        if not submitted_code:
            return Response({'error': 'Code field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not stored_code:
            return Response({'error': 'Code expired or has not been generated.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(submitted_code) == stored_code:
            cache.delete(key)
            return Response({'message': 'Payment code validated successfully. Proceed with transaction.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid code submitted.'}, status=status.HTTP_400_BAD_REQUEST)
