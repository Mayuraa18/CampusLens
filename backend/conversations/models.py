from django.db import models
from django.contrib.auth.models import User
from documents.models import Document
# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chats')
    title =  models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat {self.id} - {self.title} - User: {self.user.username} - Document: {self.document.title}"

class Message(models.Model):
    class Role(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} - Role: {self.role} - Chat: {self.chat.id}"