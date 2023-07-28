
from django.db import models
import uuid

class BaseModel(models.Model):



    class Meta:
        abstract=True