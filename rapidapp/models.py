from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image


# Create your models here.

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.rating}/5"



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.email

class Ambulance(models.Model):
    ambulance_number = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100)
    driver_number = models.CharField(null=True, max_length=15)
    driver_cnic = models.CharField(null=True, max_length=15)
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.ambulance_number


class EmergencyRequest(models.Model):
    EMERGENCY_TYPE_CHOICES = [
        ('Emergency', 'Emergency'),
        ('Non-Emergency', 'Non-Emergency'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('dispatched', 'Dispatched'),
        ('on_route', 'On Route'),
        ('Pickedup', 'Pickedup'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ambulance = models.ForeignKey(Ambulance, null=True, on_delete=models.SET_NULL)
    hospital_name = models.CharField(max_length=255)
    customer_mobile = models.CharField(max_length=15)
    pickup_address = models.TextField()
    emergency_type = models.CharField(max_length=50, choices=EMERGENCY_TYPE_CHOICES)
    request_time = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('Accepted', 'Accepted'), ('enroute', 'Enroute'), ('completed', 'Completed')], default='Pending')

    def __str__(self):
        return f'{self.user.username} (ID: {self.user.id}) - {self.emergency_type}'




class MedicalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    search_fields = ['user__id', 'user__username']

    def __str__(self):
        return f"{self.user.username} (ID: {self.user.id}) Medical Profile"

# Medicine product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

# Cart model for storing items
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

# Order Item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"



# ----------------------------------Driver/emts--------------------------------------------

class Driver(AbstractUser):
     # Add related_name arguments to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='driver_set',  # Changed related_name to avoid conflict with User model
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='driver_permissions_set',  # Changed related_name to avoid conflict with User model
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_driver = models.BooleanField(default=True, verbose_name="Driver Status")  # Custom field to identify drivers
    
    def __str__(self):
        return self.username  # Customize the display for admin



        