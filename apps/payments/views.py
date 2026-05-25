from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from decimal import Decimal


def _calc_fee(vacancy):
    s_min = vacancy.salary_min or Decimal('0')
    s_max = vacancy.salary_max or Decimal('0')
    if s_min == 0 and s_max == 0:
        return Decimal('0')
    avg = (s_min + s_max) / 2 if s_max else s_min
    return (avg * Decimal('0.001')).quantize(Decimal('0.01'))


@login_required
def unpaid_list_view(request):
    if request.user.role != 'employer':
        return redirect('vacancies:list')
    try:
        employer = request.user.employer
    except Exception:
        return redirect('employers:profile')

    from apps.vacancies.models import Application
    unpaid = Application.objects.filter(
        vacancy__employer=employer,
        status='accepted',
        is_paid=False
    ).select_related('vacancy', 'resume', 'resume__applicant')

    total = sum(a.fee or 0 for a in unpaid)

    return render(request, 'payments/unpaid_list.html', {
        'unpaid':   unpaid,
        'total':    total,
        'employer': employer,
    })


@login_required
@transaction.atomic
def pay_all_view(request):
    if request.method != 'POST' or request.user.role != 'employer':
        return redirect('payments:unpaid_list')
    try:
        employer = request.user.employer
    except Exception:
        return redirect('employers:profile')

    from apps.vacancies.models import Application
    from .models import Payment

    unpaid = Application.objects.filter(
        vacancy__employer=employer,
        status='accepted',
        is_paid=False,
        fee__isnull=False
    ).select_related('vacancy', 'resume__applicant')

    if not unpaid.exists():
        messages.warning(request, 'Нет неоплаченных откликов.')
        return redirect('payments:unpaid_list')

    total = sum(a.fee for a in unpaid)

    snapshot = [
        {
            'application_id': a.id,
            'vacancy':        a.vacancy.title,
            'applicant':      a.resume.applicant.get_full_name(),
            'fee':            str(a.fee),
        }
        for a in unpaid
    ]

    Payment.objects.create(
        employer=employer,
        amount=total,
        status='paid',
        applications_snapshot=snapshot,
    )

    unpaid.update(is_paid=True)

    messages.success(request, f'Оплачено {len(snapshot)} откликов на сумму {total} ₽.')
    return redirect('payments:unpaid_list')
