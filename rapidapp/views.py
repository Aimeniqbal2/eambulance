from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from .models import Ambulance, EmergencyRequest, MedicalProfile, EmergencyRequest, Product, CartItem, Order, OrderItem, Feedback
from .form import EmergencyRequestForm, RegisterForm, LoginForm, ProfileUpdateForm, MedicalProfileForm, FeedbackForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# UpdateEmailForm, CustomPasswordChangeForm,
def driverdashboard(request):
    return render(request, 'rapidapp/DriverDashboard.html')

def home(request):
    return render(request, 'rapidapp/home.html')

def services(request):
    return render(request, 'rapidapp/services.html')

def welcomeservice(request):
    return render(request, 'rapidapp/welcomeservice.html')

def welcomecontact(request):
    return render(request, 'rapidapp/welcomecontact.html')

def about(request):
    return render(request, 'rapidapp/aboutus.html')

def contact(request):
    return render(request, 'rapidapp/contact.html')


def base_view(request):
    return render(request, 'rapidapp/base.html')


def send_message_view(request):
    return render(request, 'rapidapp/send_message.html')


def success_page(request):
    return render(request, 'rapidapp/success_page.html')


def error_page(request):
    return render(request, 'rapidapp/error_page.html')

def feedback_success(request):
    return render(request, 'rapidapp/feedback_success.html')

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_success')  # Redirect to a success page
    else:
        form = FeedbackForm()
    
    return render(request, 'rapidapp/submit_feedback.html', {'form': form})


# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         u_form = UpdateEmailForm(request.POST, instance=request.user)
#         p_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             update_session_auth_hash(request, p_form.user)  # Important to keep the user logged in after password change
#             return redirect('profile_update_success')
#     else:
#         u_form = UpdateEmailForm(instance=request.user)
#         p_form = CustomPasswordChangeForm(user=request.user)

#     return render(request, 'Rapidapp/profile_edit.html', {
#         'u_form': u_form,
#         'p_form': p_form
#     })


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         user_form = UpdateUserForm(request.POST, instance=request.user)
#         profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect(to='profile')
#     else:
#         user_form = UpdateUserForm(instance=request.user)
#         profile_form = UpdateProfileForm(instance=request.user.profile)

#     return render(request, 'Rapidapp/profile.html', {'user_form': user_form, 'profile_form': profile_form})


# class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
#     template_name = 'Rapidapp/change_password.html'
#     success_message = "Successfully Changed Your Password"
#     success_url = reverse_lazy('home')


# class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
#     template_name = 'Rapidapp/password_reset.html'
#     email_template_name = 'Rapidapp/password_reset_email.html'
#     subject_template_name = 'Rapidapp/password_reset_subject'
#     success_message = "We've emailed you instructions for setting your password, " \
#                       "if an account exists with the email you entered. You should receive them shortly." \
#                       " If you don't receive an email, " \
#                       "please make sure you've entered the address you registered with, and check your spam folder."
#     success_url = reverse_lazy('home')

# Register View
# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created successfully.')
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'Rapidapp/register.html')

class registerView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'rapidapp/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(registerView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, 'rapidapp/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, 'rapidapp/login.html', {'form': form})


# Login View
# def login_view(request):
#     try:
#         if request.method == "POST":
#             # Get the post parameters
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Successfully Logged In")
#                 return redirect('Rapidapp/home')

#             else:
#                 messages.warning(request, "Invalid credentials! Please try again")
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     except Exception as e:
#         print(f"{e}")
#     return render(request, 'Rapidapp/login.html')


class login_View(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(login_View, self).form_valid(form)

    # first
    # if request.user.is_authenticated:
    #     user = request.user
    #     try:
    #         profile = user.Profile
    #     except profile.DoesNotExist:
    #         # Create the profile if it doesn't exist
    #         profile = Profile.objects.create(user=user)

    # # If the request is a POST, process the login form
    # if request.method == 'POST':
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = request.POST.get('username')
    #         password = request.POST.get('password')
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             auth_login(request, user)  # Log the user in
    #             return redirect('home')  # Redirect to home page after successful login
    #         else:
    #             messages.error(request, 'Invalid username or password.')
    # else:
    #     form = AuthenticationForm()  # Display the empty login form

    # # Render the login page with the form
    # return render(request, 'Rapidapp/login.html', {'form': form})


# Logout View
def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'rapidapp/profile.html', {'form': form})

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Important! To keep the user logged in after password change
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'rapidapp/password_change.html', {'form': form})




def request_ambulance(request):
    if request.method == 'POST':
        form = EmergencyRequestForm(request.POST)
        if form.is_valid():
            # Find the first available ambulance
            ambulance = Ambulance.objects.filter(is_available=True).first()

            if ambulance:
                if ambulance.is_available:
                    # Process the request and mark the ambulance as unavailable
                    ambulance.is_available = False
                    ambulance.save()

                    # Create and save the emergency request
                    emergency_request = form.save(commit=False)
                    emergency_request.ambulance = ambulance
                    emergency_request.user = request.user
                    emergency_request.save()
                     # Notify drivers about the new request
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'driver_requests',
                    {
                        'type': 'send_request_update',
                        'request_id': emergency_request.id,
                        'user': request.user.username,
                        'address': emergency_request.pickup_address,
                        'status': emergency_request.status,
                    }
                )


                    # Send a success message
                messages.success(request, "Ambulance has been booked successfully.")
                    
                    # Return the success page with a WebSocket connection
                return render(request, 'rapidapp/success_page.html', {
                        'request_id': emergency_request.id,  # Pass the request ID to the template
                    })
            else:
                # No available ambulance found
                messages.error(request, "No available ambulances found at the moment. Please try again later.")
                return redirect('error_page')  # Redirect to an error page
        else:
            # Form is not valid
            messages.error(request, "There was an error with your request. Please try again.")
            return render(request, 'rapidapp/request_ambulance.html', {'form': form})
    else:
        form = EmergencyRequestForm()
        return render(request, 'rapidapp/request_ambulance.html', {'form': form})

def driver_requests(request):
    return render(request, 'rapidapp/driver_requests.html')


@login_required
def medical_profile_view(request):
    try:
        medical_profile = request.user.medicalprofile
    except MedicalProfile.DoesNotExist:
        medical_profile = None

    if request.method == 'POST':
        form = MedicalProfileForm(request.POST, instance=medical_profile)
        if form.is_valid():
            medical_profile = form.save(commit=False)
            medical_profile.user = request.user
            medical_profile.save()
            return redirect('medical_profile')
    else:
        form = MedicalProfileForm(instance=medical_profile)

    return render(request, 'rapidapp/medical_profile.html', {'form': form, 'medical_profile': medical_profile})

def track_view(request):
    orders = EmergencyRequest.objects.filter(user=request.user)
    return render(request, 'rapidapp/track.html', {'orders': orders})


def send_message_to_driver(request):
    if request.method == 'POST':
        form = DriverMessageForm(request.POST)
        if form.is_valid():
            driver_email = form.cleaned_data['driver_email']
            message = form.cleaned_data['message']
            
            # Send message to WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'driver_group',  # Create a group for drivers
                {
                    'type': 'send_message',
                    'message': message
                }
            )
    else:
        form = DriverMessageForm()
    return render(request, 'admin/send_message.html', {'form': form})



    # ----------------------------------shop--------------------------------------->


# Shop view
def shop_view(request):
    products = Product.objects.all()
    return render(request, 'rapidapp/shop.html', {'products': products})

# Add to cart view
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f'{product.name} added to your cart.')
    return redirect('shop')

# View Cart
@login_required
def cart_view(request):
    cart_items = request.session.get('cart', [])
    total_price = 0
    items = []

    for item in cart_items:
        product = get_object_or_404(Product, id=item['product_id'])
        item_total = product.price * item['quantity']
        total_price += item_total
        items.append({'product': product, 'quantity': item['quantity'], 'total': item_total})

    return render(request, 'rapidapp/cart.html', {'cart_items': items, 'total_price': total_price})

# Checkout View
@login_required
def checkout_view(request):
    cart_items = request.session.get('cart', [])
    total_price = 0
    items = []

    for item in cart_items:
        product = get_object_or_404(Product, id=item['product_id'])
        item_total = product.price * item['quantity']
        total_price += item_total
        items.append({'product': product, 'quantity': item['quantity'], 'total': item_total})

    return render(request, 'rapidapp/checkout.html', {'cart_items': items, 'total_price': total_price})

# Order Tracking View
@login_required
def track_order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'rapidapp/track_order.html', {'orders': orders})