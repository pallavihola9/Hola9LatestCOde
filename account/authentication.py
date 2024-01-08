# # authentication.py

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from account.models import User

# max_allowed_devices = 3

# class CustomTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):
#         token = User.objects.filter(key=key).first()

#         if not token:
#             raise AuthenticationFailed('Token is Invalid!')

#         if token.is_expired():
#             raise AuthenticationFailed('Token has expired')

#         if self.user and token.user != self.user:
#             raise AuthenticationFailed('Invalid token for this user')

#         # Calculate the number of active devices for the user
#         active_devices_count = User.objects.filter(user=token.user).count()

#         # Check if the user has reached the device limit
#         if active_devices_count >= max_allowed_devices:
#             # Log out the oldest session by deleting the token
#             oldest_token = User.objects.filter(user=token.user).order_by('created_at').first()
#             oldest_token.delete()
#             raise AuthenticationFailed('User reached the maximum device limit. Oldest session logged out.')

#         return token.user, token
