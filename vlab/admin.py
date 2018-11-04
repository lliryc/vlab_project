from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from vlab.models import OrgUser, Device, DeviceOutputParameter, Experiment, ExperimentCondition, ExperimentOutputParameter, ExperimentSourceRequirement, LabInfo, DeviceInfo
from vlab.models import Qualification, QualificationCheckpoint, QualificationOrgRequirement, LabQualification, QualificationOrgCheckpoint, QualificationDeviceRequirement, QualificationDeviceCheckpoint
class VLabAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = 'Панель администрирования'

    # Text to put in each page's <h1> (and above login form).
    site_header = 'Администрирование VLAB'

    # Text to put at the top of the admin index page.
    index_title = 'Администрирование сайта'

admin_site = VLabAdminSite()
admin_site.site_header = 'VLAB'

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', widget=forms.TextInput)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput)

    class Meta:
        model = OrgUser
        fields = ('org', 'email', 'first_name',
            'second_name', 'last_name',
            'role_lab', 'role_customer', 'subrole_customer' )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = OrgUser
        fields = ('org', 'email', 'password', 'first_name',
            'last_name',
            'role_lab', 'role_customer',
            'subrole_customer',
            'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('org', 'email', 'password',
        'first_name', 'last_name',
        'role_lab', 'role_customer',
        'is_admin', 'verified')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Разрешения', {'fields': ('is_admin','verified')}),
        ('Персональная информация', {'fields': ('org','first_name',
            'last_name', 'role_lab',
            'role_customer','subrole_customer')
            }),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

#class OrgAdmin(admin.ModelAdmin):
#     list_display = ('name', 'short_desc', 'qty', 'status', 'type')


# Now register the new UserAdmin...
admin.site.register(OrgUser, UserAdmin)
admin.site.register(LabInfo)
admin.site.register(DeviceInfo)
admin.site.register(Device)
admin.site.register(DeviceOutputParameter)
admin.site.register(Experiment)
admin.site.register(ExperimentCondition)
admin.site.register(ExperimentOutputParameter)
admin.site.register(ExperimentSourceRequirement)

admin.site.register(Qualification)
admin.site.register(QualificationCheckpoint)
admin.site.register(QualificationOrgCheckpoint)
admin.site.register(QualificationDeviceCheckpoint)
admin.site.register(QualificationOrgRequirement)
admin.site.register(LabQualification)
admin.site.register(QualificationDeviceRequirement)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


#class Admin(admin.ModelAdmin):
#    prepopulated_fields = {'slug': ('name',)}



# Register your models here.
#from vlab.models import Food_Category, Food_Component, Mix, Nutrition_Value, UserProfile, Delivery, Order
#admin.site.register(Food_Category)
#admin.site.register(Food_Component, FoodComponentAdmin)
