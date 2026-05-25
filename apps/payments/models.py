from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid',    'Оплачено'),
        ('failed',  'Ошибка'),
    ]

    employer              = models.ForeignKey(
                                'employers.Employer',
                                on_delete=models.CASCADE,
                                related_name='payments'
                            )
    amount                = models.DecimalField('Сумма', max_digits=12, decimal_places=2)
    status                = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='pending')
    applications_snapshot = models.JSONField('Отклики (snapshot)', default=list)
    created_at            = models.DateTimeField(auto_now_add=True)
    updated_at            = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'payments'
        verbose_name        = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.employer.company_name} — {self.amount} ₽ ({self.get_status_display()})'
