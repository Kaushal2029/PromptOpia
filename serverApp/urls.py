
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from serverApp import views
from .views import *
from knox import views as knox_views

# router = routers.DefaultRouter()
# router.register(r'users',views.UserViewSet)
# router.register(r'groups',views.GroupViewSet)
# router.register(r'texts',views.PromptTextViewSet)



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),

# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('loginss/', views.user_login),
    # path('logout/', views.user_logout),
    # path('register/', views.user_register),
    # path('forgot_password/', views.forgot_password),
    path('prompt_text_form/<int:service_id>', views.prompt_text_form,name='prompt_text'),
    # path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),  # Define the URL pattern for reset_password with placeholders for uidb64 and token
    path('prompt-text/',PromptTextView.as_view(), name='example'),
    path('prompt-text/<int:id>',PromptTextView.as_view(), name='example'),
    path('login/',UserLoginView.as_view(),name="login"),
    path('logout/',knox_views.LogoutView.as_view(), name='logout'),#in-built classs is provided by knox
    path('forget-password/',ForgetPasswordView.as_view(), name='forget_password'),
    path('register/',RegisterView.as_view(),name="register"),

]