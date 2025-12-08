import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
message_requests = {} # In-memory storage (for demo purposes


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time (24hr format)
        current_hour = datetime.now().hour

        # Allowed window: 6 AM (06:00) to 9 PM (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "❌ Access to chats is restricted between 9 PM and 6 AM."
            )

        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track POST requests to /messages/ (sending chat messages)
        if request.method == "POST" and "messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize tracking for IP
            if ip not in message_requests:
                message_requests[ip] = []

            # Filter out timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            message_requests[ip] = [
                ts for ts in message_requests[ip] if ts > one_minute_ago
            ]

            # Check if limit exceeded (5 messages in 1 minute)
            if len(message_requests[ip]) >= 5:
                return HttpResponseForbidden(
                    "🚫 You have exceeded the limit of 5 messages per minute."
                )

            # Otherwise, log this message timestamp
            message_requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check if the user is authenticated
        if request.user.is_authenticated:
            # Assuming your custom User model has a `role` field
            user_role = getattr(request.user, "role", None)

            # Deny access if not admin or moderator
            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        response = self.get_response(request)
        return response