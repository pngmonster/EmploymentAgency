from django.db import models
from django.conf import settings


class Employer(models.Model):
    user           = models.OneToOneField(
                         settings.AUTH_USER_MODEL,
                         on_delete=models.CASCADE,
                         related_name='employer'
                     )
    company_name   = models.CharField('Название компании', max_length=255)
    inn            = models.CharField('ИНН', max_length=20, blank=True, unique=True, null=True)
    industry       = models.CharField('Сфера деятельности', max_length=150, blank=True)
    founded_year   = models.PositiveSmallIntegerField('Год основания', null=True, blank=True)
    website        = models.URLField('Сайт', blank=True)
    logo           = models.ImageField('Логотип', upload_to='logos/', blank=True, null=True)
    about          = models.TextField('Об организации', blank=True)
    is_verified    = models.BooleanField('Подтверждена', default=False)
    phone          = models.CharField('Телефон', max_length=30, blank=True)
    contact_person = models.CharField('Контактное лицо', max_length=255, blank=True)
    country        = models.CharField('Страна', max_length=100, blank=True)
    city           = models.CharField('Город', max_length=100, blank=True)
    address        = models.CharField('Адрес', max_length=255, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'employers'
        verbose_name        = 'Работодатель'
        verbose_name_plural = 'Работодатели'

    def __str__(self):
        return self.company_name

    def years_on_market(self):
        if self.founded_year:
            from django.utils import timezone
            return timezone.now().year - self.founded_year
        return None
