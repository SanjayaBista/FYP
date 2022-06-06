from django import forms
from .models import Customer


class RegisterForm(forms.ModelForm):

    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), min_length=6)
    confirmPassword = forms.CharField(label='confirmPassword',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}), min_length=6)
    condition  = forms.BooleanField(required=True)
    class Meta:
        model = Customer
        fields = ['first_name','last_name', 'email','phone_number','password','username']
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')
        if password != confirmPassword:
            raise forms.ValidationError('Passwords don\'t match')
        # email = self.cleaned_data.get('email')
        # try:
        #     Customer.objects.get(email=email)
        #     raise forms.ValidationError(
        #         'Email already exists'
        #     )
        # except Customer.DoesNotExist:
        #     pass
    def clean_email(self):
        # Get the email
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    def __init__(self, *args, **kargs):
        super(RegisterForm, self).__init__(*args, **kargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last name'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'User Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
        self.fields['condition'].widget.attrs.update({'id': 'checkbox1'})