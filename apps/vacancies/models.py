from django.db import models
from apps.employers.models import Employer
from apps.applicants.models import Resume


class Vacancy(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time',  'Полная занятость'),
        ('part_time',  'Частичная занятость'),
        ('internship', 'Стажировка'),
        ('contract',   'Договор'),
        ('freelance',  'Фриланс'),
    ]
    SCHEDULE_CHOICES = [
        ('five_days', 'Пятидневка'),
        ('shift',     'Сменный'),
        ('flexible',  'Гибкий'),
        ('remote',    'Удалённый'),
    ]
    WORK_FORMAT_CHOICES = [
        ('office', 'Офис'),
        ('remote', 'Удалённо'),
        ('hybrid', 'Гибрид'),
    ]
    STATUS_CHOICES = [
        ('active', 'Активная'),
        ('paused', 'Приостановлена'),
        ('closed', 'Закрыта'),
    ]

    employer         = models.ForeignKey(
                           Employer, on_delete=models.CASCADE,
                           related_name='vacancies'
                       )
    title            = models.CharField('Название вакансии', max_length=255)
    about            = models.TextField('Описание', blank=True)
    experience_years = models.PositiveSmallIntegerField('Требуемый опыт (лет)', default=0)
    salary_min       = models.DecimalField('ЗП от', max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max       = models.DecimalField('ЗП до', max_digits=12, decimal_places=2, null=True, blank=True)
    employment_type  = models.CharField(
                           'Тип занятости', max_length=15,
                           choices=EMPLOYMENT_TYPE_CHOICES, default='full_time'
                       )
    schedule         = models.CharField(
                           'График', max_length=15,
                           choices=SCHEDULE_CHOICES, default='five_days'
                       )
    work_format      = models.CharField(
                           'Формат работы', max_length=10,
                           choices=WORK_FORMAT_CHOICES, default='office'
                       )
    country          = models.CharField('Страна', max_length=100, blank=True)
    city             = models.CharField('Город', max_length=100, blank=True)
    address          = models.CharField('Адрес', max_length=255, blank=True)
    contact_name     = models.CharField('Контактное лицо', max_length=255, blank=True)
    contact_phone    = models.CharField('Телефон', max_length=30, blank=True)
    contact_email    = models.EmailField('Email', blank=True)
    status           = models.CharField(
                           'Статус', max_length=10,
                           choices=STATUS_CHOICES, default='active'
                       )
    expires_at       = models.DateField('Актуальна до', null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'vacancies'
        verbose_name        = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.title} — {self.employer.company_name}'

    def salary_display(self):
        if self.salary_min and self.salary_max:
            return f'{int(self.salary_min):,} – {int(self.salary_max):,} ₽'
        elif self.salary_min:
            return f'от {int(self.salary_min):,} ₽'
        elif self.salary_max:
            return f'до {int(self.salary_max):,} ₽'
        return 'По договорённости'

    def applications_count(self):
        return self.applications.count()


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Ожидает рассмотрения'),
        ('viewed',   'Просмотрено'),
        ('accepted', 'Приглашение'),
        ('rejected', 'Отказ'),
    ]

    vacancy          = models.ForeignKey(
                           Vacancy, on_delete=models.CASCADE,
                           related_name='applications'
                       )
    resume           = models.ForeignKey(
                           Resume, on_delete=models.CASCADE,
                           related_name='applications'
                       )
    cover_letter     = models.TextField('Сопроводительное письмо', blank=True)
    status           = models.CharField(
                           'Статус', max_length=10,
                           choices=STATUS_CHOICES, default='pending'
                       )
    employer_comment = models.TextField('Комментарий работодателя', blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'applications'
        verbose_name        = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering            = ['-created_at']
        constraints         = [
            models.UniqueConstraint(
                fields=['vacancy', 'resume'],
                name='uq_application'
            )
        ]

    def __str__(self):
        return f'{self.resume.applicant} → {self.vacancy.title}'
