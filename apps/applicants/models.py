from django.db import models
from django.conf import settings


class Applicant(models.Model):
    GENDER_CHOICES = [
        ('male',   'Мужской'),
        ('female', 'Женский'),
        ('other',  'Другой'),
    ]
    STATUS_CHOICES = [
        ('actively_looking', 'Активно ищу работу'),
        ('open_to_offers',   'Рассматриваю предложения'),
        ('not_looking',      'Не ищу работу'),
    ]

    user          = models.OneToOneField(
                        settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                        related_name='applicant'
                    )
    last_name     = models.CharField('Фамилия', max_length=100)
    first_name    = models.CharField('Имя', max_length=100)
    middle_name   = models.CharField('Отчество', max_length=100, blank=True)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    gender        = models.CharField('Пол', max_length=10, choices=GENDER_CHOICES, blank=True)
    phone         = models.CharField('Телефон', max_length=30, blank=True)
    avatar        = models.ImageField('Фото', upload_to='avatars/', blank=True, null=True)
    country       = models.CharField('Страна', max_length=100, blank=True)
    city          = models.CharField('Город', max_length=100, blank=True)
    address       = models.CharField('Адрес', max_length=255, blank=True)
    about         = models.TextField('О себе', blank=True)
    status        = models.CharField(
                        'Статус поиска', max_length=20,
                        choices=STATUS_CHOICES,
                        default='actively_looking'
                    )
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'applicants'
        verbose_name        = 'Соискатель'
        verbose_name_plural = 'Соискатели'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)


class ApplicantPassport(models.Model):
    applicant  = models.OneToOneField(
                     Applicant, on_delete=models.CASCADE,
                     related_name='passport'
                 )
    series     = models.CharField('Серия', max_length=20, blank=True)
    number     = models.CharField('Номер', max_length=30)
    scan       = models.FileField('Скан', upload_to='passports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'applicant_passports'
        verbose_name        = 'Паспорт'
        verbose_name_plural = 'Паспорта'

    def __str__(self):
        return f'Паспорт {self.applicant}'


class ApplicantWorkBook(models.Model):
    applicant  = models.OneToOneField(
                     Applicant, on_delete=models.CASCADE,
                     related_name='work_book'
                 )
    number     = models.CharField('Номер', max_length=30)
    scan       = models.FileField('Скан', upload_to='workbooks/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'applicant_work_books'
        verbose_name        = 'Трудовая книжка'
        verbose_name_plural = 'Трудовые книжки'

    def __str__(self):
        return f'Трудовая {self.applicant}'


class Resume(models.Model):
    EDUCATION_CHOICES = [
        ('no_education',      'Без образования'),
        ('secondary',         'Среднее'),
        ('vocational',        'Среднее специальное'),
        ('incomplete_higher', 'Неполное высшее'),
        ('bachelor',          'Бакалавр'),
        ('master',            'Магистр'),
        ('phd',               'Кандидат/доктор наук'),
    ]
    STATUS_CHOICES = [
        ('active',   'Активное'),
        ('hidden',   'Скрытое'),
        ('archived', 'В архиве'),
    ]

    applicant        = models.ForeignKey(
                           Applicant, on_delete=models.CASCADE,
                           related_name='resumes'
                       )
    title            = models.CharField('Желаемая должность', max_length=255)
    experience_years = models.PositiveSmallIntegerField('Опыт (лет)', default=0)
    salary_expected  = models.DecimalField(
                           'Желаемая ЗП', max_digits=12,
                           decimal_places=2, null=True, blank=True
                       )
    education        = models.CharField(
                           'Образование', max_length=20,
                           choices=EDUCATION_CHOICES, blank=True
                       )
    skills           = models.TextField('Навыки', blank=True)
    resume_pdf       = models.FileField('Резюме PDF', upload_to='resumes/', blank=True, null=True)
    status           = models.CharField(
                           'Статус', max_length=10,
                           choices=STATUS_CHOICES, default='active'
                       )
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'resumes'
        verbose_name        = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.title} — {self.applicant}'
