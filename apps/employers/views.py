from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Q
from .models import Employer
from .forms import EmployerProfileForm


def _get_or_none(user):
    try:
        return user.employer
    except Employer.DoesNotExist:
        return None


@login_required
def profile_view(request):
    if request.user.role != 'employer':
        return redirect('applicants:profile')

    employer = _get_or_none(request.user)
    form = EmployerProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=employer
    )

    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, 'Профиль компании сохранён.')
        return redirect('employers:profile')

    return render(request, 'employers/profile.html', {
        'form': form,
        'employer': employer,
    })


@login_required
def stats_view(request):
    if request.user.role != 'employer':
        return redirect('vacancies:list')

    employer = _get_or_none(request.user)
    if not employer:
        messages.warning(request, 'Сначала заполните профиль компании.')
        return redirect('employers:profile')

    from apps.vacancies.models import Application, Vacancy
    from apps.payments.models import Payment

    # Вакансии с количеством откликов
    vacancies = Vacancy.objects.filter(employer=employer).annotate(
        total_apps=Count('applications'),
        accepted=Count('applications', filter=Q(applications__status='accepted')),
        pending=Count('applications', filter=Q(applications__status='pending')),
        rejected=Count('applications', filter=Q(applications__status='rejected')),
    ).order_by('-created_at')

    # Общая статистика
    total_apps     = Application.objects.filter(vacancy__employer=employer).count()
    total_accepted = Application.objects.filter(vacancy__employer=employer, status='accepted').count()
    total_paid     = Payment.objects.filter(employer=employer, status='paid').aggregate(s=Sum('amount'))['s'] or 0
    unpaid_count   = Application.objects.filter(vacancy__employer=employer, status='accepted', is_paid=False).count()
    unpaid_sum     = Application.objects.filter(
                         vacancy__employer=employer, status='accepted', is_paid=False
                     ).aggregate(s=Sum('fee'))['s'] or 0

    # Последние отклики с данными соискателей
    recent_apps = Application.objects.filter(
        vacancy__employer=employer
    ).select_related(
        'vacancy', 'resume', 'resume__applicant'
    ).order_by('-created_at')[:20]

    # Города соискателей
    from apps.applicants.models import Applicant
    cities = (
        Applicant.objects
        .filter(resumes__applications__vacancy__employer=employer)
        .values('city')
        .annotate(cnt=Count('id'))
        .exclude(city='')
        .order_by('-cnt')[:6]
    )

    # Образование соискателей
    educations = (
        Application.objects
        .filter(vacancy__employer=employer)
        .values('resume__education')
        .annotate(cnt=Count('id'))
        .exclude(resume__education='')
        .order_by('-cnt')
    )

    import json
    from apps.applicants.models import Resume
    edu_map = dict(Resume.EDUCATION_CHOICES)
    edu_labels = [edu_map.get(e['resume__education'], e['resume__education']) for e in educations]
    edu_data   = [e['cnt'] for e in educations]

    city_labels = [c['city'] or 'Не указан' for c in cities]
    city_data   = [c['cnt'] for c in cities]

    return render(request, 'employers/stats.html', {
        'employer':       employer,
        'vacancies':      vacancies,
        'total_apps':     total_apps,
        'total_accepted': total_accepted,
        'total_paid':     total_paid,
        'unpaid_count':   unpaid_count,
        'unpaid_sum':     unpaid_sum,
        'recent_apps':    recent_apps,
        'edu_labels_json': json.dumps(edu_labels),
        'edu_data_json':   json.dumps(edu_data),
        'city_labels_json': json.dumps(city_labels),
        'city_data_json':   json.dumps(city_data),
    })
