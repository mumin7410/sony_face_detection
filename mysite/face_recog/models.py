from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import os

# Create your models here.
class Member(models.Model):
  Name = models.CharField(max_length=255)
  Active = models.BooleanField(default=False)
  Location = models.CharField(max_length=255)
  date_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.Name

class EmployeeInfo(models.Model):
  EmployeeID = models.IntegerField()
  FirstName = models.CharField(max_length=255)
  LastName = models.CharField(max_length=255)

  def __str__(self):
    return self.EmployeeID

class Transaction(models.Model):
  autoID = models.AutoField(primary_key=True)
  EmployeeID = models.IntegerField()  # Assuming EmployeeID is an integer, you can adjust accordingly
  Name = models.CharField(max_length=255)
  DateTime = models.DateTimeField()
  CameraNo = models.IntegerField()  # Assuming CameraNo is an integer, you can adjust accordingly
  Image = models.ImageField(upload_to='transaction_images/')  # Adjust the upload_to path as needed

  def __str__(self):
    return f"{self.EmployeeID} - {self.Name} - {self.DateTime}"

@receiver(pre_delete, sender=Transaction)
def delete_transaction_image(sender, instance, **kwargs):
    # Delete the associated image file when a Transaction record is deleted
    if instance.Image:
        if os.path.isfile(instance.Image.path):
            os.remove(instance.Image.path)