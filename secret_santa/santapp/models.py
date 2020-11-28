from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    vk_id = models.IntegerField(unique=True)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    registration_time = models.DateTimeField(auto_now_add=True)

    data_available_time = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=256)
    wishlist = models.CharField(max_length=1024)

    present_to = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
