from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serverApp.models import PromptText
from serverApp.serializers import PromptTextCreateSerializer, PromptTextSerializer,RegisterSerializer, UserLoginSerializer
from django.utils.encoding import smart_bytes
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer






# class UserLoginView(APIView):
    # def post(self, request):
    #     email = request.data.get('email')
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         user_id = User.objects.filter(username=username).values('id','username','email')
    #         return Response({"success": user_id}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"failed": "Username or password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)


class UserLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        temp_list = super(UserLoginView, self).post(request)
        temp_list.data['id'] = user.id
        temp_list.data['username'] = user.username
        temp_list.data['email'] = user.email
       
        return Response(temp_list.data)



@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'success': 'Logged out successfully'})


class RegisterView(APIView):
     serializer_class = RegisterSerializer
     
     def post(self,reuqest):
        serializer =RegisterSerializer(data=reuqest.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({"Success":"User Registered Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



         


class PromptTextView(APIView):
    serializer_class = PromptTextSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = self.request.user.id
        queryset = PromptText.objects.filter(user=user)
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def post(self, request):
        data = request.data
        user_id = self.request.user.id
        content = data.get('content')  
        title = data.get('title') 
        if user_id is None:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = PromptText.objects.create(content=content, title=title,user_id=user_id)
        serializer = PromptTextCreateSerializer(queryset)
        return Response(serializer.data,status=status.HTTP_200_OK,)

    
    def put(self, request,id):
        data = request.data
        queryset = PromptText.objects.get(id = id)
        queryset.content = data.get('content')
        queryset.title = data.get('title')
        queryset.save()
        serializer = PromptTextCreateSerializer(queryset)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request):
        data = request.data
        queryset = PromptText.objects.get(id = data.get('id'))
        queryset.delete()
        return Response({'success': 'Data deleted successfully'})

class ForgetPasswordView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]

    def post(self,request):
        data = request.data
        # user = self.request.user.id
        user = User.objects.get(email=data.get('email'))
        user.set_password(data.get('password'))
        user.save()
        return Response({"success":"password Resest"})


@api_view(['POST'])
def prompt_text_form(request, service_id):
    if request.method == "POST":
        title = request.data.get('title')
        content = request.data.get('content')
        user_id = request.user.id
        serializer = PromptTextSerializer(data=request.data)
        if serializer.is_valid():
            save = PromptText.objects.create(
                content=content,
                title=title,
                service_id=service_id,
                user_id=user_id,
            )
            print("Data Stored----------", save)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['POST'])
# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.data.get('email')  # Extract email from request data
#         if not email:
#             return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         user = User.objects.filter(email=email).first()
#         if user:
#             # Generate token
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.pk))
#             token = default_token_generator.make_token(user)
#             # Build reset password link
#             reset_link = request.build_absolute_uri(
#                 f'/reset-password/{uidb64}/{token}/'
#             )
#             return Response({'reset_link': reset_link}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#     else:
#         return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['POST'])
# def reset_password(request, uidb64, token):
#     # Decode the user ID from uidb64
#     try:
#         uid = smart_bytes(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     # Check if the user and token are valid
#     if user is not None and default_token_generator.check_token(user, token):
#         # Get the new password from the request data
#         new_password = request.data.get('new_password')

#         # Set the new password
#         user.set_password(new_password)
#         user.save()

#         return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request, uidb64, token):
    # Decode the user ID from uidb64
    try:
        uid = smart_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the user and token are valid
    if user is not None and default_token_generator.check_token(user, token):
        # Get the new password from the request data
        new_password = request.data.get('new_password')

        # Set the new password
        user.set_password(new_password)
        user.save()  # Save the user with the new password
        print("----",user.save())

        return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

