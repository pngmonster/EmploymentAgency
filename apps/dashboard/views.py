from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import timedelta
import json


@staff_member_required(login_url='/accounts/login/')
def dashboard_view(request):
    from apps.accounts.models import User
    from apps.applicants.models import Applicant, Resume
    from apps.employers.models import Employer
    from apps.vacancies.models import Vacancy, Application
    from apps.payments.models import Payment

    now      = timezone.now()
    days_30  = now - timedelta(days=30)
    days_7   = now - timedelta(days=7)

    stats = {
        'users_total':        User.objects.count(),
        'users_week':         User.objects.filter(created_at__gte=days_7).count(),
        'applicants_total':   Applicant.objects.count(),
        'employers_total':    Employer.objects.count(),
        'employers_verified': Employer.objects.filter(is_verified=True).count(),
        'vacancies_active':   Vacancy.objects.filter(status='active').count(),
        'vacancies_total':    Vacancy.objects.count(),
        'resumes_total':      Resume.objects.count(),
        'apps_total':         Application.objects.count(),
        'apps_accepted':      Application.objects.filter(status='accepted').count(),
        'apps_pending':       Application.objects.filter(status='pending').count(),
        'revenue_total':      Payment.objects.filter(status='paid').aggregate(s=Sum('amount'))['s'] or 0,
        'revenue_month':      Payment.objects.filter(status='paid', created_at__gte=days_30).aggregate(s=Sum('amount'))['s'] or 0,
        'payments_count':     Payment.objects.filter(status='paid').count(),
    }

    reg_qs = (
        User.objects
        .filter(created_at__gte=days_30)
        .annotate(day=TruncDay('created_at'))
        .values('day', 'role')
        .annotate(cnt=Count('id'))
        .order_by('day')
    )
    reg_days = sorted(set(r['day'].strftime('%d.%m') for r in reg_qs))
    reg_appl = {r['day'].strftime('%d.%m'): r['cnt'] for r in reg_qs if r['role'] == 'applicant'}
    reg_empl = {r['day'].strftime('%d.%m'): r['cnt'] for r in reg_qs if r['role'] == 'employer'}

    app_by_status = list(Application.objects.values('status').annotate(cnt=Count('id')))
    status_labels = [dict(Application.STATUS_CHOICES).get(a['status'], a['status']) for a in app_by_status]
    status_data   = [a['cnt'] for a in app_by_status]

    revenue_qs = (
        Payment.objects.filter(status='paid')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    rev_labels = [r['month'].strftime('%b %Y') for r in revenue_qs]
    rev_data   = [float(r['total']) for r in revenue_qs]

    top_employers = (
        Employer.objects
        .annotate(
            vac_count=Count('vacancies'),
            accepted_count=Count('vacancies__applications', filter=Q(vacancies__applications__status='accepted')),
            revenue=Sum('payments__amount', filter=Q(payments__status='paid'))
        )
        .order_by('-vac_count')[:10]
    )

    recent_payments = Payment.objects.select_related('employer').order_by('-created_at')[:10]
    recent_users    = User.objects.order_by('-created_at')[:10]

    return render(request, 'dashboard/index.html', {
        'stats':              stats,
        'reg_days_json':      json.dumps(reg_days),
        'reg_appl_json':      json.dumps([reg_appl.get(d, 0) for d in reg_days]),
        'reg_empl_json':      json.dumps([reg_empl.get(d, 0) for d in reg_days]),
        'status_labels_json': json.dumps(status_labels),
        'status_data_json':   json.dumps(status_data),
        'rev_labels_json':    json.dumps(rev_labels),
        'rev_data_json':      json.dumps(rev_data),
        'top_employers':      top_employers,
        'recent_payments':    recent_payments,
        'recent_users':       recent_users,
    })
