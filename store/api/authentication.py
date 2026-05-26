from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User 
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken




class CookieJWTAuthentication(BaseAuthentication):
    def authentication(self,request):
        token = request.COOKIES.get("access_token")
        if not token:
            return None
        
        try:
           payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureerror:
           raise AuthenticationFailed("Token expired")
        except jwt.DecodeError:
           raise AuthenticationFailed("Invalid token")
        
        try:
           user = User.objects.get(id=payload["user_id"])
        except user.doesNotExist:
           
            raise AuthenticationFailed("Invalid or expired token")
        return (user, None)
        
        
       