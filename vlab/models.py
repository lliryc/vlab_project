from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime
from datetime import date
from vlab import choices

# Create your models here.

class OrgUserManager(BaseUserManager):

    def create_user(self, org, email, first_name, second_name, last_name, role_lab, role_customer, subrole_customer, verified, last_login, date_joined, password=None):
        if not email:
            raise ValueError('Не указан email')

        user = self.model(
            org = org,
            email=self.normalize_email(email),
            first_name=first_name,
            second_name=second_name,
            last_name=last_name,
            role_lab = role_lab,
            role_customer = role_customer,
            subrole_customer = subrole_customer,
            verified = verified,
            last_login = last_login,
            date_joined = date_joined
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, org, email, first_name, second_name, last_name, role_lab, role_customer, subrole_customer, verified, last_login, date_joined, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            org = org,
            email=self.normalize_email(email),
            password = password,
            first_name=first_name,
            second_name=second_name,
            last_name=last_name,
            role_lab = role_lab,
            role_customer = role_customer,
            subrole_customer = subrole_customer,
            verified = verified,
            last_login=last_login,
            date_joined=date_joined
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Org(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    img_url = models.ImageField(upload_to = 'org_profiles/')
    city = models.CharField(max_length = 128)
    country = models.CharField(max_length = 128)
    address = models.CharField(max_length = 256)
    contact_name = models.CharField(max_length = 128)
    email = models.EmailField(max_length = 200)
    phone = models.CharField(max_length = 20)
    fax = models.CharField(max_length = 20)
    site = models.CharField(max_length = 256)
    score = models.FloatField()

    class Meta:
        verbose_name_plural = 'orgs'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class OrgUserRole(models.Model):
    role = models.CharField(max_length=128,
                     choices = choices.USER_ROLE_CHOICES)

    def __str__(self):
        return self.role

class OrgUser(AbstractBaseUser):
    org = models.ForeignKey(Org, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length = 128, unique=True)
    first_name = models.CharField(max_length = 128)
    second_name = models.CharField(max_length = 128)
    last_name = models.CharField(max_length = 128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role_lab = models.BooleanField(default=False)
    role_customer = models.BooleanField(default=True)
    subrole_customer = models.ManyToManyField(OrgUserRole)
    date_joined = models.DateTimeField(default=datetime.now(), null=True, blank=True)
    last_login = models.DateTimeField(default=datetime.now(), null=True, blank=True)
    verified = models.BooleanField(default=False)

    objects = OrgUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Document(models.Model):
    name = models.CharField(max_length = 256)
    file = models.FileField(upload_to='docs/')
    for_deleting = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'documents'

    def __str__(self):
        return self.name

# class Org(models.Model):
#     user = models.OneToOneField(
#             User,
#             on_delete=models.CASCADE,
#             primary_key=True,
#     )
#     name = models.CharField(max_length = 128, unique=True)
#     contact_name = models.CharField(max_length = 128)
#     img_url = models.CharField(max_length = 128)
#     city = models.CharField(max_length = 128)
#     country = models.CharField(max_length = 128)
#     address = models.CharField(max_length = 256)
#     phone = PhoneNumberField(blank = True)
#     fax = PhoneNumberField(blank = True)
#     site = models.CharField(max_length = 256)
#     email = models.EmailField(max_length = 20)
#     role_lab = models.BooleanField(default=False)
#     role_customer = models.BooleanField(default=True)
#     score = models.FloatField()
#
#     class Meta:
#         verbose_name_plural = 'orgs'
#
#     def __str__(self):
#         return self.name

class Device(models.Model):
    name = models.CharField(max_length = 256)
    img_url = models.ImageField(upload_to = 'device_profiles/')
    short_desc = models.CharField(max_length = 256)
    desc = models.TextField()
    manufacturer = models.CharField(max_length = 128)
    year = models.CharField(max_length = 4)
    lab = models.ForeignKey(OrgUser, on_delete=models.CASCADE)
    broken = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'devices'

    def __str__(self):
        return self.name

class DeviceOutputParameter(models.Model):
    name = models.CharField(max_length = 256)
    measure = models.CharField(max_length = 128)
    accuracy = models.CharField(max_length = 128)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'deviceoutputparameters'

    def __str__(self):
        return self.name

class Experiment(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    desc = models.TextField(max_length = 512)
    lab = models.ForeignKey(OrgUser, on_delete=models.CASCADE)
    draft = models.BooleanField(default = True)
    devices = models.ManyToManyField(Device)

    class Meta:
        verbose_name_plural = 'experiments'

    def __str__(self):
        return self.name

class ExperimentCondition(models.Model):
    name = models.CharField(max_length = 128)
    desc = models.TextField(max_length = 512)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'experimentconditions'

    def __str__(self):
        return self.name

class ExperimentSourceRequirement(models.Model):
    name = models.CharField(max_length = 256)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'experimentsourcerequirements'

    def __str__(self):
        return self.name

class ExperimentOutputParameter(models.Model):
    name = models.CharField(max_length = 256)
    measure = models.CharField(max_length = 128)
    accuracy = models.CharField(max_length = 128)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'experimentoutputparameters'

    def __str__(self):
        return self.name

# class Customer(models.Model):
#     org = models.CharField(max_length = 256)
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )
#     img_url = models.CharField(max_length = 128)
#     city = models.CharField(max_length = 128)
#     country = models.CharField(max_length = 128)
#     address = models.CharField(max_length = 256)
#     phone = models.CharField(max_length = 20)
#     fax = models.CharField(max_length = 20)
#     site = models.CharField(max_length = 256)
#     email = models.EmailField(max_length = 256)
#
#     class Meta:
#         verbose_name_plural = 'customers'
#
#     def __str__(self):
#         return self.name


class Order(models.Model):
    ticket = models.CharField(max_length = 128, unique = True)

    created = models.DateField(default = date.today)

    customer = models.ForeignKey(OrgUser, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    task_status = models.CharField(max_length = 128)

    delivery_status = models.CharField(max_length = 128)
    delivery_ticket = models.CharField(max_length = 128)
    delivery_type = models.IntegerField()

    source_origin_country = models.CharField(max_length = 128)
    source_origin_city = models.CharField(max_length = 128)
    source_origin_address = models.CharField(max_length = 256)
    source_origin_phone = models.CharField(max_length = 20)
    source_origin_responsible = models.CharField(max_length = 128)

    dest_origin_country = models.CharField(max_length = 128)
    dest_origin_city = models.CharField(max_length = 128)
    dest_origin_address = models.CharField(max_length = 256)
    dest_origin_phone = models.CharField(max_length = 20)
    dest_origin_responsible = models.CharField(max_length = 128)

    class Meta:
        verbose_name_plural = 'orders'

    def __str__(self):
        return self.ticket


class DeviceBooking(models.Model):
    start_date = models.DateField(date.today)
    end_date = models.DateField(date.today)
    device = models.ForeignKey(Device, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = 'devicebookings'

class Review(models.Model):
    reviewer = models.ForeignKey(OrgUser, null=True, on_delete = models.SET_NULL)
    score = models.FloatField()
    comments = models.TextField()
#    lab = models.ForeignKey(OrgUser, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = 'reviews'

class Problem(models.Model):
    name = models.CharField(max_length = 256)
    author = models.ForeignKey(OrgUser, null=True, on_delete = models.SET_NULL)
    desc = models.TextField()
    status = models.IntegerField(default=0)
    special_status = models.IntegerField(default=0)
    created = models.DateTimeField(default = datetime.now())
    modified = models.DateTimeField(default = datetime.now())

    class Meta:
        verbose_name_plural = 'problems'

class ProblemComment(models.Model):
    author = models.ForeignKey(OrgUser, null=True, on_delete=models.SET_NULL)
    desc = models.TextField()
    rank_status = models.IntegerField(default=0)
    created = models.DateTimeField(default = datetime.now())
    modified = models.DateTimeField(default = datetime.now())
    problem = models.ForeignKey(Problem, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = 'problemcomments'

class ProblemCommentComment(models.Model):
    author = models.ForeignKey(OrgUser, null=True, on_delete = models.SET_NULL)
    desc = models.TextField()
    rank_status = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now())
    modified = models.DateTimeField(default=datetime.now())
    problem_comment = models.ForeignKey(ProblemComment, on_delete = models.CASCADE)


    class Meta:
        verbose_name_plural = 'problemcommentcomments'

class Auction(models.Model):
    name = models.CharField(max_length = 256)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(OrgUser, on_delete=models.CASCADE)
    desc = models.TextField()
    rank_status = models.IntegerField(default=0)
    created = models.DateTimeField(default = datetime.now())
    modified = models.DateTimeField(default = datetime.now())
    documents = models.ManyToManyField(Document)

class AuctionOutputParameter(models.Model):
    name = models.CharField(max_length = 256)
    measure = models.CharField(max_length = 128)
    sufficient_accuracy = models.CharField(max_length = 128)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'auctionoutputparameters'

    def __str__(self):
        return self.name

class AuctionBid(models.Model):
    price = models.FloatField()
    documents = models.ManyToManyField(Document)
    experiment = models.OneToOneField(Experiment, on_delete=models.SET_NULL, null=True)

class Qualification(models.Model):
    name = models.CharField(max_length = 256)
    active_before_date = models.DateField(default = datetime.now())
    owner = models.ForeignKey(Org, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='qualifications'

    def __str__(self):
        return self.name

class QualificationCheckpoint(models.Model):
    name = models.CharField(max_length = 256)
    active_before_date = models.DateField()
    owner = models.ForeignKey(Org, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='qualificationCheckpoints'

    def __str__(self):
        return self.name

class QualificationOrgRequirement(models.Model):
    name = models.CharField(max_length = 256)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    template_file = models.FileField()
    type = models.IntegerField()

    class Meta:
        verbose_name_plural='qualificationOrgRequirements'

    def __str__(self):
        return self.name

class LabQualification(models.Model):
    lab = models.ForeignKey(Org, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)

class QualificationOrgCheckpoint(models.Model):
    name = models.CharField(max_length = 256)
    qualification = models.ForeignKey(LabQualification, on_delete=models.SET_NULL, null=True)
    requirement = models.ForeignKey(QualificationOrgRequirement, on_delete=models.SET_NULL, null=True)
    info_file = models.FileField()
    type = models.IntegerField()

    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='qualificationOrgCheckpoints'

    def __str__(self):
        return self.name

class QualificationDeviceRequirement(models.Model):
    name = models.CharField(max_length = 256)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    template_file = models.FileField()
    type = models.IntegerField()

    class Meta:
        verbose_name_plural='qualificationDeviceRequirements'

    def __str__(self):
        return self.name

class QualificationDeviceCheckpoint(models.Model):
    name = models.CharField(max_length = 256)
    qualification = models.ForeignKey(Qualification, on_delete=models.SET_NULL, null=True)
    requirement = models.ForeignKey(QualificationDeviceRequirement, on_delete=models.SET_NULL, null=True)
    info_file = models.FileField()
    type = models.IntegerField()
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='qualificationDeviceCheckpoints'

    def __str__(self):
        return self.name

class LabInfo(models.Model):
    title = models.CharField(max_length=500)
    desc = models.TextField(null=True)
    contact_name = models.CharField(max_length=5000, null=True)
    contact_tel = models.CharField(max_length=200, null=True)
    contact_email = models.CharField(max_length=200, null=True)
    base_org_title = models.CharField(max_length=500, null=True)
    base_org_form = models.CharField(max_length=500, null=True)
    base_org_address = models.CharField(max_length=1000, null=True)
    base_org_phone = models.CharField(max_length=200, null=True)
    base_org_fax = models.CharField(max_length=200, null=True)
    base_org_email = models.CharField(max_length=200, null=True)
    base_org_site = models.CharField(max_length=200, null=True)
    geocode = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural='labInfos'

    def __str__(self):
        return self.title

class DeviceInfo(models.Model):
    title = models.CharField(max_length=500)

    manufacturer = models.CharField(max_length=500, null=True)
    device_class = models.CharField(max_length=500, null=True)
    year = models.CharField(max_length=500, null=True)
    price_segment = models.CharField(max_length=500, null=True)
    tech_condition = models.CharField(max_length=500, null=True)
    reglament = models.CharField(max_length=1000, null=True)
    desc = models.TextField(null=True)

    contact_name = models.CharField(max_length=5000, null=True)

    base_org_title = models.CharField(max_length=500, null=True)
    base_org_form = models.CharField(max_length=500, null=True)
    base_org_address = models.CharField(max_length=1000, null=True)
    base_org_phone = models.CharField(max_length=200, null=True)
    base_org_fax = models.CharField(max_length=200, null=True)
    base_org_email = models.CharField(max_length=200, null=True)
    base_org_site = models.CharField(max_length=200, null=True)

    labinfo = models.ForeignKey(LabInfo, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural='deviceInfos'

    def __str__(self):
        return self.title

class MapCache(models.Model):
    address = models.CharField(max_length=500)
    geocode = models.CharField(max_length=200)
