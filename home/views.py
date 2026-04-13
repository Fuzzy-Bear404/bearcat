from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.files.base import ContentFile
from django import forms

# Python standard library
import os
from io import BytesIO

# Third-party imports
from PIL import Image

# Local app imports
from .models import MainPageContent, Topic, UserProfile
from .forms import RegisterForm, LoginForm, ProfileImageForm, EmailChangeForm

# Create your views here.

def index(request):
    page = MainPageContent.objects.first()   # din main content
    topics = Topic.objects.all()             # hent topics

    return render(request, "home/index.html", {
        "page": page,
        "topics": topics
    })


def registerpage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.is_active=False
            #user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully! You can log in now.")
            return redirect('home:login')
        
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "home/register.html", {'form': form})

def loginpage(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "home/login.html", {'form': form})

def logoutpage(request):
    logout(request)
    return redirect('home:login')

#@login_required(login_url='home:index')
#def user_settings(request):

#    return render(request, 'home/settings.html')
    
@login_required(login_url='home:login')
def delete_account_confirm(request):
    """Show delete account confirmation page"""
    return render(request, 'home/delete_confirm.html')

@login_required(login_url='home:login')
def delete_account(request):
    """Actually delete the account"""
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home:index')
    else:
        return redirect('home:delete_confirm')
    

@login_required(login_url='home:login')
def user_settings(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Get the uploaded file
            uploaded_file = request.FILES.get('profile_image')
            
            if uploaded_file:
                # Delete old image FIRST if exists
                if profile.profile_image:
                    try:
                        if os.path.isfile(profile.profile_image.path):
                            os.remove(profile.profile_image.path)
                    except:
                        pass
                    # Clear the field to prevent Django from adding suffix
                    profile.profile_image = None
                
                # Process the image securely
                processed_image, filename = process_profile_image(
                    uploaded_file, 
                    request.user.id
                )
                
                if processed_image and filename:
                    # Save with save=False, then save the model
                    profile.profile_image.save(filename, processed_image, save=False)
                    profile.save()
                    messages.success(request, "Profile image updated successfully!")
                else:
                    messages.error(request, "Error processing image. Please try a different file.")
            else:
                form.save()
                messages.success(request, "Profile updated successfully!")
            
            return redirect('home:settings')
        else:
            messages.error(request, "Error updating profile image.")
    else:
        form = ProfileImageForm(instance=profile)
    
    return render(request, 'home/settings.html', {
        'form': form,
        'profile': profile
    })



def process_profile_image(image_file, user_id):
    """
    Securely process uploaded image:
    - Remove metadata
    - Convert to PNG
    - Rename to user_id.png
    - Resize if too large
    """
    try:
        # Open image with PIL
        img = Image.open(image_file)
        
        # Convert to RGB (removes alpha channel issues and metadata)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if image is too large (max 800x800)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to BytesIO buffer as PNG (removes all metadata)
        buffer = BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        # Create secure filename: user_id.png
        filename = f"{user_id}.png"
        
        return ContentFile(buffer.read()), filename
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None
    
@login_required
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:email_change_done')  # Redirect to success page
    else:
        form = EmailChangeForm(request.user)
    
    return render(request, 'registration/change_email.html', {'form': form})

@login_required
def email_change_done(request):
    return render(request, 'registration/email_change_done.html')