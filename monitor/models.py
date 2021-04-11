from django.db import models


# Create your models here.
class ServerGroup(models.Model):
    name = models.CharField(max_length=255)
    type = models.IntegerField()


class Server(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=1000)
    email = models.EmailField()
    server_group = models.ForeignKey(ServerGroup, on_delete=models.CASCADE)


class Notification(models.Model):
    type = models.IntegerField()
    time = models.TimeField()
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
