from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users.serializers import UserSerializer, UserLogoutSerializer


# Create your views here.
class UserRegisterApiView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return user


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status': 'success',
            'detail': "Logged out successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)