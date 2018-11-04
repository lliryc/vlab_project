from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from phonenumber_field.formfields import PhoneNumberField
from vlab.models import Device, Experiment
from vlab.models import OrgUser, Org, OrgUserRole
import json
from vlab import choices
from captcha.fields import CaptchaField

class OrgUserRegistrationForm(RegistrationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', widget=forms.TextInput)
    last_name = forms.CharField(label='Last name', widget=forms.TextInput)
    second_name = forms.CharField(label='Second name', widget=forms.TextInput)
    date_joined = forms.DateTimeField(widget=forms.HiddenInput, required=False)
    last_login = forms.DateTimeField(widget=forms.HiddenInput, required=False)
    verified = forms.BooleanField(widget=forms.HiddenInput, required=False)
#    img_url = forms.FileField(label='Photo')
    org = forms.ModelChoiceField(queryset=Org.objects.all(), widget=forms.Select, required=True)
    captcha = CaptchaField(label="Введите текст как на картинке ниже")
    print(list(org.choices))

    subrole_customer = forms.ModelMultipleChoiceField(queryset=OrgUserRole.objects.all(), widget=forms.SelectMultiple)
    print(list(subrole_customer.choices))

    class Meta:
        model = OrgUser
        fields = ('org','email', 'first_name',
            'second_name', 'last_name',
            'role_lab', 'role_customer',
            'date_joined', 'last_login',
            'verified')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def form_valid(self, form):
        res = super().form_valid(form)
        print(form.errors)
        return res

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            self.save_m2m()
        return user

class OrgForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the organization name")
    city = forms.CharField(max_length = 128)
    country = forms.CharField(max_length = 128)
    address = forms.CharField(max_length = 256)
    contact_name = forms.CharField(max_length = 128)
    email = forms.EmailField(max_length = 200)
    phone = forms.CharField(max_length = 20)
    fax = forms.CharField(max_length = 20)
    site = forms.CharField(max_length = 256)
    score = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    captcha = CaptchaField()

    class Meta:
        model = Org
        fields = ('name', 'img_url', 'city', 'country', 'address', 'contact_name', 'email', 'phone', 'fax', 'site', 'score')

class DeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('name', 'img_url', 'short_desc', 'desc', 'manufacturer', 'year', 'lab', 'broken')
    # name = models.CharField(max_length = 256)
    # img_url = models.ImageField(upload_to = 'device_profiles/')
    # short_desc = models.CharField(max_length = 256)
    # desc = models.TextField()
    # manufacturer = models.CharField(max_length = 128)
    # year = models.CharField(max_length = 4)
    # lab = models.ForeignKey(OrgUser, on_delete=models.CASCADE)
    # broken = models.BooleanField(default=False)


# from rango.models import Page, Category, UserProfile
#
# class CategoryForm(forms.ModelForm):
#     name = forms.CharField(max_length=128,
#                            help_text="Please enter the category name")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     slug = forms.CharField(widget=forms.HiddenInput(), required = False)
#
#     # An inline class to provide additional  information on the form
#     class Meta:
#         #Provide an association between the ModelForm and a model
#         model = Category
#         fields = ('name',)
#
# class PageForm(forms.ModelForm):
#     title = forms.CharField(max_length=128,
#                            help_text="Please enter the title of the page")
#     url = forms.URLField(max_length=200, help_text="Please enter the url of the page")
#
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Page
#         exclude = ('category',)
#         # Or specify fields to include
#         #fields = ('title', 'url', 'views')
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         url = cleaned_data.get('url')
#
#         # if url is not empty and doesn't start with 'http://',
#         # then prepend 'http://'
#         if url and not url.startswith('http://') or url.startswith('https://'):
#             url = 'http://' + url
#             cleaned_data['url'] = url
#
#             return cleaned_data
#

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('website', 'picture')
