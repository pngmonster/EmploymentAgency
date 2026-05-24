from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Applicant, Resume
from .forms import ApplicantProfileForm, ResumeForm


def _get_or_none(user):
    try:
        return user.applicant
    except Applicant.DoesNotExist:
        return None


@login_required
def profile_view(request):
    if request.user.role != 'applicant':
        return redirect('employers:profile')

    applicant = _get_or_none(request.user)
    form = ApplicantProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=applicant
    )

    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, 'Профиль сохранён.')
        return redirect('applicants:profile')

    return render(request, 'applicants/profile.html', {
        'form': form,
        'applicant': applicant,
    })


@login_required
def resume_list_view(request):
    if request.user.role != 'applicant':
        return redirect('employers:profile')

    applicant = _get_or_none(request.user)
    resumes = applicant.resumes.all() if applicant else []
    return render(request, 'applicants/resume_list.html', {
        'resumes': resumes,
        'applicant': applicant,
    })


@login_required
def resume_create_view(request):
    if request.user.role != 'applicant':
        return redirect('employers:profile')

    applicant = _get_or_none(request.user)
    if not applicant:
        messages.warning(request, 'Сначала заполните профиль.')
        return redirect('applicants:profile')

    form = ResumeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        resume = form.save(commit=False)
        resume.applicant = applicant
        resume.save()
        messages.success(request, 'Резюме создано.')
        return redirect('applicants:resume_list')

    return render(request, 'applicants/resume_form.html', {'form': form, 'action': 'Создать'})


@login_required
def resume_edit_view(request, pk):
    if request.user.role != 'applicant':
        return redirect('employers:profile')

    applicant = _get_or_none(request.user)
    resume = get_object_or_404(Resume, pk=pk, applicant=applicant)
    form = ResumeForm(request.POST or None, request.FILES or None, instance=resume)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Резюме обновлено.')
        return redirect('applicants:resume_list')

    return render(request, 'applicants/resume_form.html', {'form': form, 'action': 'Сохранить'})


@login_required
def resume_delete_view(request, pk):
    applicant = _get_or_none(request.user)
    resume = get_object_or_404(Resume, pk=pk, applicant=applicant)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Резюме удалено.')
    return redirect('applicants:resume_list')


@login_required
def applications_view(request):
    applicant = _get_or_none(request.user)
    from apps.vacancies.models import Application
    apps = Application.objects.filter(
        resume__applicant=applicant
    ).select_related('vacancy', 'vacancy__employer') if applicant else []
    return render(request, 'applicants/applications.html', {'apps': apps})
