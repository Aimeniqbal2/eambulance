from django.shortcuts import render, redirect, HttpResponse
from django.urls import path
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Ambulance, EmergencyRequest, MedicalProfile,  Product, Order, OrderItem, Feedback, Driver, Contact

# Register your models here

# Create a custom UserAdmin
class CustomUserAdmin(BaseUserAdmin):
    # Add 'id' to the list of displayed fields
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Add search by ID functionality
    search_fields = ('id', 'username', 'email')

# # Re-register the User model with the custom UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
admin.site.register(Ambulance)
admin.site.register(EmergencyRequest)

class MedicalProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_id', 'medical_history', 'allergies', 'emergency_contact_name', 'emergency_contact_phone']
    
    search_fields = ['user__id', 'user__username']

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

# Re-register the MedicalProfile model with the custom admin settings
admin.site.register(MedicalProfile, MedicalProfileAdmin)


admin.site.unregister(EmergencyRequest)
class EmergencyRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_id', 'ambulance', 'request_time', 'status']
    search_fields = ['user__id', 'user__username']
    list_filter = ['status']

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'
   



# Re-register EmergencyRequest with the custom admin settings
admin.site.register(EmergencyRequest, EmergencyRequestAdmin)



admin.site.site_header = "Rapid Rescue Admin Dashboard"
admin.site.site_title = "Rapid Rescue Admin"
admin.site.index_title = "Welcome to the Rapid Rescue Admin Panel"




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'status', 'total_price']
    list_filter = ['status', 'order_date']
    inlines = [OrderItemInline]
    search_fields = ['user__username', 'id']
    actions = ['mark_as_shipped', 'mark_as_delivered']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='Shipped')

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')

    mark_as_shipped.short_description = "Mark selected orders as Shipped"
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at']
    search_fields = ['user__username', 'rating']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact_number', 'address', 'is_active', 'is_driver')  # Show fields in admin list view
    search_fields = ['username', 'contact_number']  # Enable search by username or contact
    list_filter = ('is_active', 'is_driver')  # Add filters to easily manage active or inactive drivers
    ordering = ['username']  # Order drivers by username by default