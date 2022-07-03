
from .models import CustomUser,Profile
from django import forms
from .utils import SendOtpMail


class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Password") 
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Confirm Password")
  
    class Meta:
        model = CustomUser
        fields = ('email',)
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
 

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        obj = SendOtpMail(user.email)
        obj.run()

        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Password")

class otpVerifyForm(forms.Form):
    otp = forms.IntegerField( widget=forms.NumberInput(attrs={'class':'form-control'}))



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'phone', 'address', 'city',  'country', 'zipcode', 'image','is_brand_owner','is_client')
        widgets = {'class':'form-control'}
        labels = {
            'name':'Name',
            'phone':'Phone',
            'address':'Address',
            'city':'City',
            'country':'Country',
            'zipcode':'Zipcode',
            'image':'Image',
            'is_brand_owner':'Brand Owner',
            'is_client':'Client',
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        # self.fields['is_brand_owner'].widget.attrs.update({'class': 'form-control'})
        # self.fields['is_client'].widget.attrs.update({'class': 'form-control'})

    def save(self, *args, **kwargs):
        profile = super(ProfileForm, self).save(commit=False)
        profile.save()
        return profile    


class ForgotForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Email")
    def __init__(self, *args, **kwargs):
        super(ForgotForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})



class ResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Password") 
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Confirm Password")

    def is_valid(self):
        valid = super(ResetForm, self).is_valid()
        if valid:
            password1 = self.cleaned_data.get("password")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                self.add_error('password2', 'Passwords don\'t match')
                return False
        return valid and password1 == password2
  
