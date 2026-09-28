import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from admin_app.models import Job
from user_app.models import Application, Employee


class AddEmployeeDocumentTests(TestCase):
    def setUp(self):
        self.media_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        media_settings = override_settings(MEDIA_ROOT=self.media_dir.name)
        media_settings.enable()
        self.addCleanup(media_settings.disable)

        user = get_user_model().objects.create_user(username='admin', password='password')
        self.client.force_login(user)

        job = Job.objects.create(
            company_name='Example',
            job_title='Care worker',
            job_description='Care role',
            location='London',
            salary='12',
            job_type='full_time',
            employment_type='permanent',
        )
        self.application = Application.objects.create(
            job=job,
            first_name='Alex',
            surname='Smith',
            email='alex@example.com',
            phone_number='07123456789',
            ni_number='QQ123456C',
            address='1 Example Street',
            zip_code='AB12 3CD',
            dob='1990-01-01',
            passport=SimpleUploadedFile('passport.pdf', b'%PDF passport', content_type='application/pdf'),
            status='approved',
        )
        self.url = reverse('add_employee', args=[self.application.id])

    def test_right_to_work_and_extra_documents_are_optional(self):
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('onboard'))
        employee = Employee.objects.get(application=self.application)
        self.assertFalse(employee.right_to_work)
        self.assertFalse(employee.extra_documents)

    def test_right_to_work_and_extra_documents_upload(self):
        response = self.client.post(self.url, {
            'right_to_work': SimpleUploadedFile(
                'right-to-work.pdf', b'%PDF right to work', content_type='application/pdf',
            ),
            'extra_documents': SimpleUploadedFile(
                'extra.pdf', b'%PDF extra', content_type='application/pdf',
            ),
        })

        self.assertRedirects(response, reverse('onboard'))
        employee = Employee.objects.get(application=self.application)
        self.assertEqual(employee.right_to_work.name, 'employees/right_to_work/right-to-work.pdf')
        self.assertEqual(employee.extra_documents.name, 'employees/extra_documents/extra.pdf')

    def test_employee_directory_keeps_existing_details_and_adds_profile_link(self):
        employee = Employee.objects.create(application=self.application)

        response = self.client.get(reverse('our_employees'))

        self.assertContains(response, 'First Name')
        self.assertContains(response, 'Surname')
        self.assertContains(response, 'NI Number')
        self.assertContains(response, 'Address')
        self.assertContains(response, reverse('employee_detail', args=[employee.id]))
        self.assertContains(response, 'Get all details')

    def test_employee_directory_preserves_existing_passport_photo_file_link(self):
        employee = Employee.objects.create(
            application=self.application,
            passport_photo=SimpleUploadedFile(
                'portrait.png', b'png photo', content_type='image/png',
            ),
        )

        response = self.client.get(reverse('our_employees'))

        self.assertContains(response, employee.passport_photo.url)
        self.assertContains(response, 'Passport Photo')

    def test_employee_profile_shows_all_personal_details_and_uploaded_documents(self):
        employee = Employee.objects.create(
            application=self.application,
            share_code='ABC123',
            educational_qualification='Bachelor degree',
            passport_number='P1234567',
            cv=SimpleUploadedFile('cv.pdf', b'%PDF cv', content_type='application/pdf'),
        )

        response = self.client.get(reverse('employee_detail', args=[employee.id]))

        self.assertContains(response, 'Alex Smith')
        self.assertContains(response, 'alex@example.com')
        self.assertContains(response, 'ABC123')
        self.assertContains(response, 'Bachelor degree')
        self.assertContains(response, 'P1234567')
        self.assertContains(response, 'CV')
        self.assertContains(response, employee.cv.url)
        self.assertContains(response, 'employee-profile-photo')
        self.assertContains(response, 'Download / Print CV')
        self.assertContains(response, 'Employment &amp; qualifications')

    def test_employee_profile_returns_not_found_for_unknown_employee(self):
        response = self.client.get(reverse('employee_detail', args=[0]))

        self.assertEqual(response.status_code, 404)
