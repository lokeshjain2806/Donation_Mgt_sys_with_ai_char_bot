from django.utils import timezone
from urllib import request
from docx import Document
from PyPDF2 import PdfReader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.mail import send_mail
from .models import FeedbackModel, AboutModel, ServiceModel, GalleryModel, TeamModel, ContactModel, BlogModel, \
    SubscriptionModel, MyUser, VolunteerModel, DonorModel, Donation, UserInputGenai
from .forms import RegistrationForm, LoginForm, LoginOtpForm, OtpVerificationForm, SignUpFormDonor, VolunteerModelForm, \
    DonationForm, UserInputGeminiForm
from django.contrib import messages
import random
import google.generativeai as genai
from PIL import Image


# Create your views here.
class Home(View):
    def get(self, request):
        feedback = FeedbackModel.objects.all()
        blogs = BlogModel.objects.all()
        return render(request, 'base.html', {'feedback': feedback, 'blogs': blogs})

    def post(self, request):
        feedback = FeedbackModel.objects.all()
        blogs = BlogModel.objects.all()
        email = request.POST.get('mail')
        subscription = SubscriptionModel(email=email)
        subscription.save()
        subject = 'Subscription Confirmation'
        message = 'Thank you for subscribing to our newsletter!'
        from_email = 'reset9546@gmail.com'
        to_email = [email]
        send_mail(subject, message, from_email, to_email)
        return render(request, 'base.html', {'feedback': feedback, 'blogs': blogs})


def about(request):
    about = AboutModel.objects.all()
    return render(request, 'about.html', {'about': about})


def services(request):
    service = ServiceModel.objects.all()
    return render(request, 'service.html', {'service': service})


def gallery(request):
    gallery = GalleryModel.objects.all()
    return render(request, 'gallery.html', {'gallery': gallery})


def event(request):
    return render(request, 'event.html')


def team(request):
    teams = TeamModel.objects.all()
    return render(request, 'team.html', {'teams': teams})


class Login(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                a = user.is_completed
                login(request, user)
                if a is False:
                    return redirect('complete_profile')
                else:
                    login(request, user)
                    return redirect('login_view')
            else:
                messages.error(request, 'Username Or Password is invalid')
                return render(request, 'signin.html', {'form': form})
        else:
            return render(request, 'signin.html', {'form': form})


class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('mail')
        message = request.POST.get('message')
        contact = ContactModel(name=name, email=email, message=message)
        contact.save()
        subject = 'New Contact Form Submission'
        message = f'You have received a new contact form submission from {name}.\n Email: {email}.\n Message: {message}\n'
        from_email = 'reset9546@gmail.com'
        to_email = ['lokeshjain2806@gmail.com']
        send_mail(subject, message, from_email, to_email)
        return render(request, 'contact.html')

class Blog(View):
    def get(self, request, id):
        blogs = BlogModel.objects.filter(id=id)
        return render(request, 'blogdetails.html', {'blogs': blogs})


class RegistrationView(View):
    def get(self, request):
        form =RegistrationForm
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            a = MyUser.objects.filter(email=email).exists()
            user_name = form.cleaned_data['username']
            b = MyUser.objects.filter(username=user_name).exists()
            if a:
                messages.error(request, 'Email is already exist')
                return render(request, 'registration.html', {'form': form})
            if b:
                messages.error(request, 'username is already exist')
                return render(request, 'registration.html', {'form': form})
            user = MyUser.objects.create_user(
                username=user_name,
                email=email,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1'],
                type=form.cleaned_data['type'],
            )
            return redirect('login')
        else:
            return render(request, 'registration.html', {'form': form})


class OtpLogin(View):
    def get(self, request):
        form = LoginOtpForm
        return render(request, 'loginviaotp.html', {'form': form})

    def post(self, request):
        form = LoginOtpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            a = MyUser.objects.filter(username=username).exists()
            if a:
                user = MyUser.objects.get(username=username)
                num_numbers = 4
                random_numbers = []
                for i in range(num_numbers):
                    random_1_digit = random.randint(1, 9)
                    random_numbers.append(str(random_1_digit))
                otp = int(''.join(random_numbers))
                request.session['user'] = user.id
                request.session['expected_otp'] = otp
                request.session.save()
                print(otp)
                subject = 'Login Verification'
                message = f'Otp For Login: {otp}. Otp is valid for 10 minutes only.'
                from_email = 'reset9546@gmail.com'
                recipient_list = [user.email]
                fail_silently = False
                send_mail(subject, message, from_email, recipient_list, fail_silently)
                return redirect('otp_verification')


class OtpFun(View):
    def get(self, request):
        form = OtpVerificationForm
        return render(request, 'otpverification.html', {'form': form})

    def post(self, request):
        form = OtpVerificationForm(request.POST)
        entered_otp = request.POST.get('otp')
        expected_otp = request.session.get('expected_otp')
        user_id = request.session.get('user')
        user = MyUser.objects.get(id=user_id)
        if str(entered_otp) == str(expected_otp):
            a = user.is_completed
            login(request, user)
            if a is False:
                return redirect('complete_profile')
            else:
                login(request, user)
                redirect('login_view')
        else:
            messages.error(request, 'OTP Not Valid')
            return render(request, 'otpverification.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            user = MyUser.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(self.request, 'User with this email does not exist.')
            return redirect('password-reset')
        return super().form_valid(form)


class Complete_Profile(View):
    def get(self, request):
        if request.user.type == 'Is Volunteers':
            form = VolunteerModelForm
            return render(request, 'complete_profile.html', {'form': form})
        else:
            form = SignUpFormDonor
            return render(request, 'complete_profile.html', {'form': form})

    def post(self, request):
        if request.user.type == 'Is Volunteers':
            form = VolunteerModelForm(request.POST, request.FILES)
            if form.is_valid():
                volunteer_data = form.cleaned_data
                volunteer_data['user'] = request.user
                volunteer = VolunteerModel(**volunteer_data)
                volunteer.save()
                request.user.is_completed = True
                request.user.save()
                return redirect('login_view')
        else:
            form = SignUpFormDonor(request.POST,  request.FILES)
            if form.is_valid():
                donor_data = form.cleaned_data
                donor_data['user'] = request.user
                donor = DonorModel(**donor_data)
                donor.save()
                request.user.is_completed = True
                request.user.save()
                return redirect('login_view')
            return render(request, 'complete_profile.html', {'form': form})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('home')


def login_view(request):
    print(request.user.is_authenticated)
    return render(request, 'login_home.html')


class Profile(View):
    def get(self, request, pk):
        user = get_object_or_404(MyUser, pk=pk)
        if user.type == 'Is Volunteers':
            volunteer = get_object_or_404(VolunteerModel, user=user)
            form = VolunteerModelForm(instance=volunteer)
            form.fields['email_id'].widget.attrs['readonly'] = 'readonly'
        else:
            donor = get_object_or_404(DonorModel, user=user)
            form = SignUpFormDonor(instance=donor)
            form.fields['email'].widget.attrs['readonly'] = 'readonly'
        return render(request, 'profile.html', {'form': form, 'id': pk})

    def post(self, request, pk):
        user = get_object_or_404(MyUser, pk=pk)
        if user.type == 'Is Volunteers':
            volunteer = get_object_or_404(VolunteerModel, user=user)
            form = VolunteerModelForm(request.POST, instance=volunteer)
        else:
            donor = get_object_or_404(DonorModel, user=user)
            form = SignUpFormDonor(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[pk]))
        return render(request, 'profile.html', {'form': form, 'id': pk})


class PostDonaton(View):
    def get(self, request):
        form = DonationForm
        return  render(request, 'postdonation.html', {'form': form})

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            volunteer = VolunteerModel.objects.get(user=request.user)
            company_name = volunteer.company_name
            donation = form.save(commit=False)
            donation.user = request.user
            donation.company_name = company_name
            donation.save()
            return render(request, 'postdonation.html', {'form': form})
        return render(request, 'postdonation.html', {'form': form})


class CheckDonation(View):
    def get(self, request):
        current_date = timezone.now().date()
        donations = Donation.objects.filter(date_time__date__gte=current_date)
        return render(request, 'check_donation.html', {'donations': donations})


genai.configure(api_key="AIzaSyDpmbU31oTVqo6QU1WLwKXPSa3mMW_4SyU")


class Chat_Bot(View):
    def get(self, request):
        form = UserInputGeminiForm
        return render(request, 'chat_bot.html', {'form': form})

    def post(self, request):
        form = UserInputGeminiForm(request.POST, request.FILES)
        if form.is_valid():
            user_message = form.cleaned_data['user_message']
            document = form.cleaned_data['document']
            # Set up the model
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 400,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]

            # Process the document file
            content = ""
            if document:
                file_extension = document.name.lower().split('.')[-1]
                if file_extension == 'docx' or file_extension == 'pdf':
                    if file_extension == 'docx':
                        doc = Document(document)
                        for paragraph in doc.paragraphs:
                            content += paragraph.text
                    elif file_extension == 'pdf':
                        reader = PdfReader(document)
                        for page in reader.pages:
                            content += page.extract_text()
                elif file_extension == 'jpg' or file_extension == 'jpeg' or file_extension == 'png':
                    image = Image.open(document)
                    model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                                  generation_config=generation_config,
                                                  safety_settings=safety_settings)
                    response = model.generate_content([user_message, image], stream=True)
                    response.resolve()
                    bot_message =response.text
                    user_input_genai = UserInputGenai.objects.create(
                        user=request.user,
                        user_message=user_message,
                        document=document,
                        bot_message=bot_message
                    )


                    return render(request, 'chat_bot.html', {'form': form, 'bot_message': bot_message})

            model = genai.GenerativeModel(model_name="gemini-pro",
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)

            prompt_parts = [user_message + '\n' + content]
            response = model.generate_content(prompt_parts)
            bot_message = response.text
            user_input_genai = UserInputGenai.objects.create(
                user=request.user,
                user_message=user_message,
                bot_message=bot_message
            )

            return render(request, 'chat_bot.html', {'form': form, 'bot_message': bot_message})

        return render(request, 'chat_bot.html', {'form': form})

