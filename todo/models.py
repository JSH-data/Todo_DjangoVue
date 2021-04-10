from django.db import models

# Create your models here.
class Todo(models.Model) : 
    name = models.CharField('NAME', max_length=5, blank=True)
    todo = models.CharField('TODO', max_length=5, blank=True)

    def __str__(self) :  # 자체 이름 출력 admin에서 확인 가능
        return self.todo
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if(self.name == ''):
            self.name = '홍길동'
        super().save()