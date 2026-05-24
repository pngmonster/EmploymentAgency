from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
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
