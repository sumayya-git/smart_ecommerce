from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User 
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken

# from rest_framework.authentication import SessionAuthentication
# from django.middleware.csrf import CSRFCheck
# from rest_framework.exceptions import PermissionDenied


# class DebugSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         check = CSRFCheck(lambda req: None)
#         check.process_request(request)
#         reason = check.process_view(request, None, (), {})

#         print("=" * 60)
#         print("DRF CSRF DEBUG")
#         print("COOKIE:", request.COOKIES.get("csrftoken"))
#         print("HEADER:", request.META.get("HTTP_X_CSRFTOKEN"))
#         print("REASON:", reason)
#         print("=" * 60)

#         if reason:
#             raise PermissionDenied(reason)




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
        
        
       