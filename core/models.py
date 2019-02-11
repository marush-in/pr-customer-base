from django.db import models


class Profession(models.Model):
    description = models.CharField(max_length=50)

    @property
    def status(self):
        return True

    def __str__(self):
        return self.description


class DataSheet(models.Model):
    description = models.CharField(max_length=50)
    historical_data = models.TextField()

    def __str__(self):
        return self.description


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    professions = models.ManyToManyField(Profession)
    data_sheet = models.OneToOneField(
        DataSheet, on_delete=models.CASCADE, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    doc_num = models.CharField(max_length=12, unique=True)

    @property
    def status_message(self):
        if self.is_active:
            return "Customer is acitve"
        else:
            return "Customer is not acitve"

    def number_professions(self):
        return self.professions.all().count()

    def __str__(self):
        return self.name


class Document(models.Model):
    PP = 'PP'
    ID = 'ID'
    OT = 'OT'

    DOC_TYPES = (
        (PP, 'PassPort'),
        (ID, 'Identity card'),
        (OT, 'Others'),
    )

    dtype = models.CharField(choices=DOC_TYPES, max_length=2)
    doc_number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_number
