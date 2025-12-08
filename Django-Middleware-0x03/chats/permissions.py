from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission: Only allow users to access their own objects
    (e.g., conversations, messages).
    """

    def has_object_permission(self, request, view, obj):
        # For Message model
        if hasattr(obj, "sender"):
            return obj.sender == request.user

        # For Conversation model
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure only authenticated participants of a conversation
    can access or send messages in that conversation.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission:
        - For Conversations: user must be a participant
        - For Messages: user must be the sender OR a participant of the conversation
        """
        user = request.user

        # If the object is a Conversation
        if hasattr(obj, "participants"):
            # Only allow participants to read/update/delete
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return user in obj.participants.all()
            return user in obj.participants.all()

        # If the object is a Message
        if hasattr(obj, "conversation"):
            conversation = obj.conversation
            if request.method in ["PUT", "PATCH", "DELETE"]:
                # Only allow the sender OR conversation participant to modify/delete
                return obj.sender == user or user in conversation.participants.all()
            return user in conversation.participants.all()

        return False