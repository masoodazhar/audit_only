from datetime import date, datetime
from email.policy import default
from random import choices
from django.db import models

# Create your models here.

status = [
    ("Not Set", ""),
    ("confirm", "confirm"),
    ("rejected", "rejected"),
    ("Third Part", "Third Part"),
]


class BankStatement(models.Model):
    user_id = models.IntegerField()
    amount = models.FloatField()
    customer = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=30)
    date = models.DateField()
    status = models.CharField(max_length=20, default="", blank=True, choices=status)
    type = models.CharField(max_length = 10, choices=[("cr", "Credited"), ("dr","Debited")])
    comment = models.TextField()
    audit_date = models.DateField(default=datetime.now)


    def __str__(self):
        return self.customer +"->"+str(self.amount)

    def class_name(self):
        return "BankStatement"

class WithdrawalRequest(models.Model):
    user_id = models.IntegerField()
    amount = models.FloatField(default=0)
    customer = models.CharField(max_length=100, default="")
    bank_name = models.CharField(max_length=100, default="")
    date = models.DateField()
    status = models.CharField(max_length=20, default="", blank=True, choices=status)
    audit_date = models.DateField(default=datetime.now)

    def __str__(self) -> str:
        return self.customer + " -> " + str(self.user_id)

    def class_name(self):
        return "WithdrawalRequest"


class DepositRequest(models.Model):
    user_id = models.IntegerField()
    amount = models.FloatField(default=0)
    customer = models.CharField(max_length=100, default="")
    bank_name = models.CharField(max_length=100, default="")
    date = models.DateField()
    status = models.CharField(max_length=20, default="", blank=True, choices=status)
    audit_date = models.DateField(default=datetime.now)

    def __str__(self) -> str:
        return self.customer + " -> " + str(self.user_id)

    def class_name(self):
        return "DepositRequest"