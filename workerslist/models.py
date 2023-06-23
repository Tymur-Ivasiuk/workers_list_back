from django.core.exceptions import ValidationError
from django.db import models


class Worker(models.Model):
    warden = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    date_start = models.DateField()
    profession = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def recursionGetParentIds(self, instance):
        try:
            id_list = [instance.id, ]
            if instance.warden:
                id_list.extend(self.recursionGetParentIds(instance.warden))
            return id_list
        except:
            return []

    def save(self, *args, **kwargs):
        if self.id in self.recursionGetParentIds(self.warden):
            raise ValidationError('You can\'t have child as a parent!')
        if self.warden and self.warden.id == self.id:
            raise ValidationError('You can\'t have yourself as a parent!')

        return super(Worker, self).save(*args, **kwargs)
