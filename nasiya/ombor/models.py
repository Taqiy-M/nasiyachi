from django.db import models


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=50)
    # 1 is the cheapest plan, for us to decide. May be 10, 100, 1000 will be next plans
    plan = models.IntegerField(default=1)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
