from rest_framework import generics, views, response, status
from .models import User
from .permissions import IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer


class UserSignUpViews(generics.CreateAPIView):
    object = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

    
        response_data = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        return response.Response(response_data, status=status.HTTP_201_CREATED)

class UserLoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

        
            response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        return response.Response(response_data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=400)
    

class AllUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]