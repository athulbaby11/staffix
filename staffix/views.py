import random

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect

from admin_app.models import Job
from user_app.models import Application

# Create your views here.
def index(request):
    jobs = Job.objects.order_by('-id')[:6]
    return render(request, 'index.html', {'jobs': jobs})

def viewmore_job(request):
    jobs = Job.objects.order_by('-id')
    locations = Job.objects.exclude(location='').order_by('location').values_list('location', flat=True).distinct()
    return render(request, 'viewmore_job.html', {'jobs': jobs, 'locations': locations})

def job_detail(request, job_slug):
    job = get_object_or_404(Job, slug=job_slug)
    return render(request, 'job_detail.html', {'job': job})

def _new_captcha(request):
    """Store a fresh, simple addition captcha in the session and return its numbers."""
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    request.session['apply_captcha_num1'] = num1
    request.session['apply_captcha_num2'] = num2
    request.session['apply_captcha_answer'] = num1 + num2
    return num1, num2


def apply_job(request, job_slug):
    job = get_object_or_404(Job, slug=job_slug)

    if request.method == 'POST':
        errors = {}

        expected_answer = request.session.get('apply_captcha_answer')
        submitted_answer = request.POST.get('captcha', '').strip()
        if not submitted_answer or not submitted_answer.lstrip('-').isdigit() or int(submitted_answer) != expected_answer:
            errors['captcha'] = 'Incorrect captcha answer. Please try again.'

        application = Application(
            job=job,
            first_name=request.POST.get('first_name', '').strip(),
            surname=request.POST.get('surname', '').strip(),
            email=request.POST.get('email', '').strip(),
            phone_number=request.POST.get('phone_number', '').strip(),
            ni_number=request.POST.get('ni_number', '').strip().upper(),
            address=request.POST.get('address', '').strip(),
            zip_code=request.POST.get('zip_code', '').strip().upper(),
            dob=request.POST.get('dob') or None,
            passport=request.FILES.get('passport'),
        )

        try:
            application.full_clean()
        except ValidationError as exc:
            for field, messages in exc.message_dict.items():
                errors.setdefault(field, messages[0])

        num1 = request.session.get('apply_captcha_num1')
        num2 = request.session.get('apply_captcha_num2')

        if errors:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            return render(request, 'applynow.html', {'job': job, 'errors': errors, 'num1': num1, 'num2': num2})

        application.save()
        request.session.pop('apply_captcha_num1', None)
        request.session.pop('apply_captcha_num2', None)
        request.session.pop('apply_captcha_answer', None)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Application submitted successfully.'})
        return redirect('job_detail', job_slug=job.slug)

    num1, num2 = _new_captcha(request)
    return render(request, 'applynow.html', {'job': job, 'num1': num1, 'num2': num2})

def login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = None
        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user_obj = None

        if user_obj is not None:
            user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('admin_dashboard')

        error = 'Invalid email or password.'

    return render(request, 'login.html', {'error': error})

def logout(request):
    auth_logout(request)
    return redirect('login')

def aboutus(request):
    return render(request, 'about-us.html')

def contact(request):
    return render(request, 'contact.html')
