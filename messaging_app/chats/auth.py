# messaging_app/chats/auth.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Nothing custom yet — we can later subclass TokenObtainPairSerializer
