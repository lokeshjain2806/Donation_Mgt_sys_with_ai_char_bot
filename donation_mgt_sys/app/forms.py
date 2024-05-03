from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, DonorModel, VolunteerModel, Donation, UserInputGenai


class RegistrationForm(UserCreationForm):
    type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=MyUser.REGISTRATION_CHOICES,
    )

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                                widget=forms.TextInput(attrs={'class': 'form-control'})
                                )
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )

    class Meta:
        model = MyUser
        fields = ['username', 'password']


class LoginOtpForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))


class OtpVerificationForm(forms.Form):
    otp = forms.IntegerField(label='Enter Your Otp', widget=forms.TextInput(attrs={'class': 'form-control'}))


class SignUpFormDonor(forms.ModelForm):
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email Id', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    mobile_number = forms.IntegerField(label='Mobile Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    id_proof = forms.FileField(label='Aadhaar Card',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=True)
    profile_image = forms.ImageField(label='Profile Image',
                                     widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
                                     required=False)

    class Meta:
        model = DonorModel
        fields = ['profile_image', 'name', 'email', 'mobile_number', 'id_proof']


class VolunteerModelForm(forms.ModelForm):
    class Meta:
        model = VolunteerModel
        fields = ['company_image', 'company_name', 'lic_no', 'lic_doc', 'email_id', 'mobile_number']

    def __init__(self, *args, **kwargs):
        super(VolunteerModelForm, self).__init__(*args, **kwargs)
        self.fields['company_image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['lic_no'].widget.attrs.update({'class': 'form-control'})
        self.fields['lic_doc'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['email_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['mobile_number'].widget.attrs.update({'class': 'form-control'})


class DonationForm(forms.ModelForm):
    date_time = forms.DateField(widget = forms.SelectDateWidget())
    class Meta:
        model = Donation
        fields = ['donation_title', 'donation_description', 'donation_location', 'contact_information',  'date_time', 'donation_type']

        def __init__(self, *args, **kwargs):
            super(DonationForm, self).__init__(*args, **kwargs)
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class UserInputGeminiForm(forms.ModelForm):
    class Meta:
        model = UserInputGenai
        fields = ['user_message', 'document']