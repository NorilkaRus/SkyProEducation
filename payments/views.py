from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from payments.models import Payment
from payments.serializers import PaymentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
import stripe
from stripe import InvalidRequestError
from django.http import request
# Create your views here.

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_51OeeJsFwLUbQdeHr078ebwekixI2OAumCmmGC1e0spoY2M9H6eNyuQO0gHSQuC12avF7DqXi4XCgWftsgGGuvn4N00KN2tMZrF"

        user = request.data.get('user')
        date = request.data.get('date')
        course = request.data.get('course')
        lesson = request.data.get('lesson')
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')
        session = request.data.get('session')
        is_paid = request.data.get('is_paid')


        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            payment_method_types=['cash', 'transfer'],
        )

        # Создание объекта платежа и сохранение в базе данных
        self.perform_create(user, date, course, lesson,  amount, payment_method, session, is_paid)

        return Response({"message": "Платеж выполнен"}, status=status.HTTP_201_CREATED)

    def perform_create(self, user, date, course, lesson,  amount, payment_method, session, is_paid):
        Payments.objects.create(
            user=user,
            date=date,
            course=course_paid,
            lesson=lesson_paid_id,
            amount=amount,
            payment_method=payment_method,
            session=session,
            is_paid=is_paid,
        )


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ['date']


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_object(self):
        payment_id = Payments.session_id

        stripe.api_key = "sk_test_51OeeJsFwLUbQdeHr078ebwekixI2OAumCmmGC1e0spoY2M9H6eNyuQO0gHSQuC12avF7DqXi4XCgWftsgGGuvn4N00KN2tMZrF"

        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_id)

            return payment_intent
        except stripe.error.InvalidRequestError:
            raise InvalidRequestError("Платеж не найден")


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()