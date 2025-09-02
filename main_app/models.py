from django.db import models
from django.contrib.auth.models import User


class College(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    

class PC(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(
        max_length=20, choices=[('connected', 'Connected'), ('disconnected', 'Disconnected')]
    )
    system_condition = models.CharField(
        max_length=20, choices=[('active', 'Active'), ('repair', 'Repair')]
    )

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pc = models.ForeignKey(PC, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=[('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')]
    )
    duration = models.DurationField()
    expiry = models.DateTimeField()
    uri = models.URLField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='bookings/', null=True, blank=True)
    num_of_devices = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Violation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pc = models.ForeignKey(PC, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(
        max_length=20, choices=[('minor', 'Minor'), ('moderate', 'Moderate'), ('major', 'Major')]
    )
    reason = models.CharField(max_length=255)
    resolved = models.BooleanField(default=False)


class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sent_chats', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_chats', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('sent', 'Sent'), ('delivered', 'Delivered'), ('read', 'Read')])
    timestamp = models.DateTimeField(auto_now_add=True)