from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import models
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Job
from user_app.models import Application, Employee

# Create your views here.
def load_admin_app(request):
    return HttpResponse("Admin App Loaded")

@login_required(login_url='login')
def register_job(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        job_type = request.POST.get('job_type')
        employment_type = request.POST.get('employment_type')

        job = Job(
            company_name=company_name,
            job_title=job_title,
            job_description=job_description,
            location=location,
            salary=salary,
            job_type=job_type,
            employment_type=employment_type
        )
        job.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Job registered successfully.'})
        return HttpResponse("Job Registered Successfully")
    return render(request, 'registerjob.html')

@login_required(login_url='login')
def register_view(request):
    jobs = Job.objects.all().order_by('-id')
    return render(request, 'register_view.html', {'jobs': jobs})

@login_required(login_url='login')
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.company_name = request.POST.get('company_name')
        job.job_title = request.POST.get('job_title')
        job.job_description = request.POST.get('job_description')
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary')
        job.job_type = request.POST.get('job_type')
        job.employment_type = request.POST.get('employment_type')
        job.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Job updated successfully.'})
        return redirect('register_view')
    return render(request, 'edit_job.html', {'job': job})

@login_required(login_url='login')
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Job deleted successfully.'})
        return redirect('register_view')
    return redirect('register_view')

@login_required(login_url='login')
def view_applications(request):
    applications = Application.objects.select_related('job').filter(status='pending').order_by('-id')
    return render(request, 'view_applications.html', {'applications': applications})

@login_required(login_url='login')
def approve_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        application.status = 'approved'
        application.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Application approved successfully.'})
        return redirect('view_applications')
    return redirect('view_applications')

@login_required(login_url='login')
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        application.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Application deleted successfully.'})
        return redirect('view_applications')
    return redirect('view_applications')

@login_required(login_url='login')
def onboard(request):
    applications = Application.objects.select_related('job').select_related('employee').filter(status='approved').order_by('-id')
    search_query = request.GET.get('q', '').strip()
    if search_query:
        applications = applications.filter(
            models.Q(first_name__icontains=search_query) | models.Q(surname__icontains=search_query)
        )
    return render(request, 'onboard.html', {'applications': applications, 'search_query': search_query})

@login_required(login_url='login')
def delete_onboard(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        application.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Application deleted successfully.'})
        return redirect('onboard')
    return redirect('onboard')

@login_required(login_url='login')
def add_employee(request, application_id):
    application = get_object_or_404(Application, id=application_id, status='approved')
    employee = Employee.objects.filter(application=application).first()

    if request.method == 'POST':
        if employee is None:
            employee = Employee(application=application)

        employee.share_code = request.POST.get('share_code', '').strip()
        employee.educational_qualification = request.POST.get('educational_qualification', '').strip()
        employee.passport_number = request.POST.get('passport_number', '').strip()

        if request.FILES.get('cv'):
            employee.cv = request.FILES.get('cv')
        if request.FILES.get('passport_photo'):
            employee.passport_photo = request.FILES.get('passport_photo')
        if request.FILES.get('dbs_certificate'):
            employee.dbs_certificate = request.FILES.get('dbs_certificate')
        if request.FILES.get('pcc_certificate'):
            employee.pcc_certificate = request.FILES.get('pcc_certificate')
        if request.FILES.get('right_to_work'):
            employee.right_to_work = request.FILES.get('right_to_work')
        if request.FILES.get('extra_documents'):
            employee.extra_documents = request.FILES.get('extra_documents')

        errors = {}
        try:
            employee.full_clean()
        except ValidationError as exc:
            for field, messages in exc.message_dict.items():
                errors.setdefault(field, messages[0])

        if errors:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            return render(request, 'add_employee.html', {'application': application, 'employee': employee, 'errors': errors})

        employee.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Employee details saved successfully.'})
        return redirect('onboard')

    return render(request, 'add_employee.html', {'application': application, 'employee': employee})

@login_required(login_url='login')
def our_employees(request):
    employees = Employee.objects.select_related('application', 'application__job').order_by('-id')
    search_query = request.GET.get('q', '').strip()
    if search_query:
        employees = employees.filter(
            models.Q(application__first_name__icontains=search_query) | models.Q(application__surname__icontains=search_query)
        )
    return render(request, 'our_employees.html', {'employees': employees, 'search_query': search_query})

@login_required(login_url='login')
def employee_detail(request, employee_id):
    employee = get_object_or_404(
        Employee.objects.select_related('application', 'application__job'),
        id=employee_id,
    )
    return render(request, 'employee_detail.html', {'employee': employee})

@login_required(login_url='login')
def admin_dashboard(request):
    jobs = Job.objects.all()
    applications = Application.objects.select_related('job').all()
    total_employees = Employee.objects.count()

    total_jobs = jobs.count()
    total_applications = applications.count()
    pending_count = applications.filter(status='pending').count()
    approved_count = applications.filter(status='approved').count()
    full_time_count = jobs.filter(job_type='full_time').count()
    part_time_count = jobs.filter(job_type='part_time').count()

    top_jobs = (
        applications.values('job__id', 'job__job_title', 'job__company_name')
        .annotate(application_count=Count('id'))
        .order_by('-application_count')[:5]
    )
    recent_applications = applications.order_by('-created_at')[:5]
    recent_jobs = jobs.order_by('-id')[:5]

    approval_rate = round((approved_count / total_applications) * 100) if total_applications else 0

    context = {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'full_time_count': full_time_count,
        'part_time_count': part_time_count,
        'top_jobs': top_jobs,
        'recent_applications': recent_applications,
        'recent_jobs': recent_jobs,
        'approval_rate': approval_rate,
        'total_employees': total_employees,
    }
    return render(request, 'dashboard.html', context)
