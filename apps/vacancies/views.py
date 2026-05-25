from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal

from .models import Vacancy, Application
from .forms import VacancyForm, ApplicationForm


def _calc_fee(vacancy):
    s_min = vacancy.salary_min or Decimal('0')
    s_max = vacancy.salary_max or Decimal('0')
    if s_min == 0 and s_max == 0:
        return None
    avg = (s_min + s_max) / 2 if s_max else s_min
    return (avg * Decimal('0.001')).quantize(Decimal('0.01'))


def vacancy_list_view(request):
    vacancies = Vacancy.objects.filter(status='active').select_related('employer')
    city   = request.GET.get('city', '').strip()
    fmt    = request.GET.get('format', '').strip()
    query  = request.GET.get('q', '').strip()
    if city:  vacancies = vacancies.filter(city__icontains=city)
    if fmt:   vacancies = vacancies.filter(work_format=fmt)
    if query: vacancies = vacancies.filter(title__icontains=query)
    return render(request, 'vacancies/list.html', {
        'vacancies': vacancies,
        'city': city, 'format': fmt, 'query': query,
        'work_format_choices': Vacancy.WORK_FORMAT_CHOICES,
    })


def vacancy_detail_view(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk, status='active')
    already_applied = False
    form = None

    if request.user.is_authenticated and request.user.role == 'applicant':
        try:
            applicant = request.user.applicant
        except Exception:
            applicant = None

        if applicant:
            already_applied = Application.objects.filter(
                vacancy=vacancy, resume__applicant=applicant
            ).exists()
            if not already_applied:
                form = ApplicationForm(request.POST or None, applicant=applicant)
                if request.method == 'POST' and form.is_valid():
                    app = form.save(commit=False)
                    app.vacancy = vacancy
                    app.save()
                    messages.success(request, 'Отклик отправлен!')
                    return redirect('vacancies:detail', pk=pk)

    return render(request, 'vacancies/detail.html', {
        'vacancy': vacancy, 'form': form, 'already_applied': already_applied,
    })


@login_required
def vacancy_my_list_view(request):
    if request.user.role != 'employer':
        return redirect('vacancies:list')
    try:
        employer = request.user.employer
    except Exception:
        messages.warning(request, 'Сначала заполните профиль компании.')
        return redirect('employers:profile')
    vacancies = employer.vacancies.all()
    return render(request, 'vacancies/my_list.html', {'vacancies': vacancies})


@login_required
def vacancy_create_view(request):
    if request.user.role != 'employer':
        return redirect('vacancies:list')
    try:
        employer = request.user.employer
    except Exception:
        messages.warning(request, 'Сначала заполните профиль компании.')
        return redirect('employers:profile')

    form = VacancyForm(request.POST or None)
    fee_preview = None

    if request.method == 'POST':
        s_min = request.POST.get('salary_min', '').strip()
        s_max = request.POST.get('salary_max', '').strip()
        try:
            mn = Decimal(s_min) if s_min else Decimal('0')
            mx = Decimal(s_max) if s_max else Decimal('0')
            if mn or mx:
                avg = (mn + mx) / 2 if mx else mn
                fee_preview = (avg * Decimal('0.001')).quantize(Decimal('0.01'))
        except Exception:
            pass

        if form.is_valid() and 'preview' not in request.POST:
            vacancy = form.save(commit=False)
            vacancy.employer = employer
            vacancy.save()
            messages.success(request, 'Вакансия опубликована.')
            return redirect('vacancies:my_list')

    return render(request, 'vacancies/form.html', {
        'form': form, 'action': 'Опубликовать', 'fee_preview': fee_preview,
    })


@login_required
def vacancy_edit_view(request, pk):
    if request.user.role != 'employer':
        return redirect('vacancies:list')
    try:
        employer = request.user.employer
    except Exception:
        return redirect('employers:profile')

    vacancy = get_object_or_404(Vacancy, pk=pk, employer=employer)
    form = VacancyForm(request.POST or None, instance=vacancy)
    fee_preview = _calc_fee(vacancy)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Вакансия обновлена.')
        return redirect('vacancies:my_list')

    return render(request, 'vacancies/form.html', {
        'form': form, 'action': 'Сохранить', 'fee_preview': fee_preview,
    })


@login_required
def vacancy_applications_view(request, pk):
    if request.user.role != 'employer':
        return redirect('vacancies:list')
    try:
        employer = request.user.employer
    except Exception:
        return redirect('employers:profile')

    vacancy = get_object_or_404(Vacancy, pk=pk, employer=employer)
    applications = vacancy.applications.select_related('resume', 'resume__applicant').all()
    return render(request, 'vacancies/applications.html', {
        'vacancy': vacancy, 'applications': applications,
    })


@login_required
def application_status_view(request, pk):
    if request.user.role != 'employer':
        return redirect('vacancies:list')

    application = get_object_or_404(
        Application, pk=pk, vacancy__employer__user=request.user
    )

    if request.method == 'POST':
        status  = request.POST.get('status')
        comment = request.POST.get('employer_comment', '')
        if status in dict(Application.STATUS_CHOICES):
            application.status = status
            application.employer_comment = comment
            if status == 'accepted' and application.fee is None:
                application.fee = _calc_fee(application.vacancy)
            application.save()
            messages.success(request, 'Статус отклика обновлён.')

    return redirect('vacancies:applications', pk=application.vacancy.pk)
