from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.http import Http404
from deepface import DeepFace
import random
from PIL import Image
import numpy as np
import os
import io
from django.conf import settings

# Create your views here.


def rand1():
    list2 = {"git": "https://github.com/sid-3q5",
             "link": "https://www.linkedin.com/in/siddhant-chauhan-4614041b9/"}
    list3 = [list2]
    return random.choice(list3)


def home(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Create profile
            photo = form.cleaned_data.get('photo')
            profile = Profile.objects.create(user=user, photo=photo)
            print("Profile Created")

            # Sending activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate account'
            message = render_to_string('home/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'f': rand1(),  # Not sure where rand1() comes from, you may need to define it
                'domain': "{0}".format("http://127.0.0.1:8000"),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.mixed_subtype = 'related'
            email.send()

            return render(request, 'home/confirm.html')
    else:
        form = SignupForm()
    return render(request, 'home/index.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        captured_image = request.FILES.get('image')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                profile_photo = profile.photo.path
                with open(profile_photo, 'rb') as f:
                    reference_image_data = f.read()
                # Convert the reference image bytes into an image
                reference_image = Image.open(io.BytesIO(reference_image_data))
                # Convert the captured image bytes into an image
                captured_image_data = captured_image.read()
                captured_image = Image.open(io.BytesIO(captured_image_data))
                # Convert images to numpy arrays
                reference_image_np = np.array(reference_image)
                captured_image_np = np.array(captured_image)

                result = DeepFace.verify(
                    img1_path=reference_image_np, img2_path=captured_image_np)
                if result['verified']:
                    print("Verification completed")
                    return redirect(f"profile/{profile.user.id}/")
                else:
                    print("User not authorized")
                    return redirect("login")
            except Profile.DoesNotExist:
                # Handle the case where the user doesn't have a profile
                raise Http404("Profile matching query does not exist.")
        else:
            # Handle invalid credentials
            context = {'error': True}
            return render(request, 'home/login.html', context)
    else:
        context = {'error': False}
        return render(request, 'home/login.html', context)


def profile(request, pk):
    if request.user.is_authenticated:
        user_data = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user_data)

        context = {"user_data": user_data,
                   "profile": profile}
        return render(request, 'home/profile.html', context)

    else:
        return redirect("login")


def logout(request):
    auth.logout(request)
    return redirect("/login")
