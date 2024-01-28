from django.shortcuts import render
from rest_framework import generics
from users.serializers import UserSerializer
from users.models import User
from django.contrib.auth.views import LoginView, LogoutView
#from users.forms import RegisterForm
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView, TemplateView, View
from django.urls import reverse_lazy, reverse
from users.forms import RegisterForm
# Create your views here.
class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserLogin(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('education/index.html')
#
#
class UserLogout(LogoutView):
    model = User
    success_url = reverse_lazy('education/index.html')
#
#
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('education/index.html')

    def form_valid(self, form):
        user = form.save()
        user.is_active=False
        user.save()
#
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
#
#         current_site = '127.0.0.1:8000'
#
#         send_mail(
#             subject='Регистрация на платформе',
#             message=f"Завершите регистрацию, перейдя по ссылке: http://{current_site}{activation_url}",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email]
#         )
#         return redirect('users:email_confirmation_sent')