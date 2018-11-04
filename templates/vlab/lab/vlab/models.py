from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.

class Document(models.Model):
    name = models.CharField(max_length = 256)
    file = models.FileField(upload_to='docs/')
    for_deleting = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'documents'

    def _str_(self):
        return self.name

class Lab(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
    )
    name = models.CharField(max_length = 128, unique=True)
    contact_name = models.CharField(max_length = 128)
    img_url = models.CharField(max_length = 128)
    city = models.CharField(max_length = 128)
    country = models.CharField(max_length = 128)
    address = models.CharField(max_length = 256)
    phone = models.CharField(max_length = 20)
    fax = models.CharField(max_length = 20)
    site = models.CharField(max_length = 256)
    email = models.EmailField(max_length = 20)
    score = models.FloatField()

    class Meta:
        verbose_name_plural = 'labs'

    def _str_(self):
        return self.name


class Experiment(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    desc = models.TextField(max_length = 512)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    deprecated = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = 'experiments'

    def _str_(self):
        return self.name

class ExperimentCondition(models.Model):
    name = models.CharField(max_length = 128)
    desc = models.TextField(max_length = 512)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'experimentconditions'

    def _str_(self):
        return self.name

class ExperimentSourceRequirement(models.Model):
    name = models.CharField(max_length = 256)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'experimentsourcerequirements'

    def _str_(self):
        return self.name

class ExperimentOutputParameter(models.Model):
    name = models.CharField(max_length = 256)
    measure = models.CharField(max_length = 128)
    accuracy = models.CharField(max_length = 128)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'experimentoutputparameters'

    def _str_(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length = 256)
    img_url = models.CharField(max_length = 128)
    short_desc = models.CharField(max_length = 256)
    desc = models.TextField()
    manufacturer = models.CharField(max_length = 128)
    year = models.CharField(max_length = 4)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    experiments = models.ManyToManyField(Experiment)
    broken = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'devices'

    def _str_(self):
        return self.name

class Customer(models.Model):
    org = models.CharField(max_length = 256)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    img_url = models.CharField(max_length = 128)
    city = models.CharField(max_length = 128)
    country = models.CharField(max_length = 128)
    address = models.CharField(max_length = 256)
    phone = models.CharField(max_length = 20)
    fax = models.CharField(max_length = 20)
    site = models.CharField(max_length = 256)
    email = models.EmailField(max_length = 256)

    class Meta:
        verbose_name_plural = 'customers'

    def _str_(self):
        return self.name


class Order(models.Model):
    ticket = models.CharField(max_length = 128, unique = True)

    date = models.DateField()

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
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

    def _str_(self):
        return self.ticket


class DeviceBooking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    device = models.ForeignKey(Device, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = 'devicebookings'

class Review(models.Model):
    reviewer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    score = models.FloatField()
    comments = models.TextField()
    lab = models.ForeignKey(Lab, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = 'reviews'

class Problem(models.Model):
    name = models.CharField(max_length = 256)
    author = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    desc = models.TextField()
    status = models.IntegerField(default=0)
    special_status = models.IntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'problems'

class ProblemComment(models.Model):
    author = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    desc = models.TextField()
    rank_status = models.IntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    problem = models.ForeignKey(Problem, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = 'problemcomments'

class ProblemCommentComment(models.Model):
    author = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    desc = models.TextField()
    rank_status = models.IntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    problem_comment = models.ForeignKey(ProblemComment, on_delete = models.CASCADE)


    class Meta:
        verbose_name_plural = 'problemcommentcomments'

class Auction(models.Model):
    name = models.CharField(max_length = 256)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(Customer, on_delete=models.CASCADE)
    desc = models.TextField()
    rank_status = models.IntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    documents = models.ManyToManyField(Document)

class AuctionOutputParameter(models.Model):
    name = models.CharField(max_length = 256)
    measure = models.CharField(max_length = 128)
    sufficient_accuracy = models.CharField(max_length = 128)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'auctionoutputparameters'

    def _str_(self):
        return self.name

class AuctionBid(models.Model):
    price = models.FloatField()
    documents = models.ManyToManyField(Document)
    experiment = models.OneToOneField(Experiment, on_delete=models.SET_NULL, null=True)

class LabInfo(models.Model):
    title = models.CharField(max_length=500)
    desc = models.TextField()
    contact_name = models.CharField(max_length=5000)
    contact_tel = models.CharField(max_length=25)
    contact_email = models.CharField(max_length=200)
    base_org_title = models.CharField(max_length=500)
    base_org_form = models.CharField(max_length=500)
    base_org_address = models.CharField(max_length=1000)
    base_org_phone = models.CharField(max_length=25)
    base_org_fax = models.CharField(max_length=25)
    base_org_email = models.CharField(max_length=200)
    base_org_site = models.CharField(max_length=200)

class MapCache(models.Model):
    address = models.CharField(max_length=500)
    geocode = models.CharField(max_length=200)
