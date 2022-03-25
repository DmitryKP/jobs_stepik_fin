from django.db import models
from django.contrib.auth.models import User
from jobs.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company', null=True, blank=True)


class Specialty(models.Model):
    code = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR,  null=True)


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=64)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=64)
    written_phone = models.CharField(max_length=32)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume', null=True, blank=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)

    class STATUS(models.TextChoices):
        NOFIND = 'no', "Не ищу работу"
        PFIND = 'look', "Рассматриваю предложения"
        AFIND = 'search', "Ищу работу"
    status = models.CharField(max_length=64, choices=STATUS.choices, null=True, blank=True)
    salary = models.IntegerField()
    specialty = models.CharField(max_length=64)

    class GRADE(models.TextChoices):
        BEG = 'beg', "Стажер"
        JUN = 'jun', "Джуниор"
        MID = 'mid', "Миддл"
        SIN = 'sin', "Синьор"
        LID = 'lead', "Лид"
    grade = models.CharField(max_length=64, choices=GRADE.choices, null=True, blank=True)
    education = models.CharField(max_length=64)
    experience = models.CharField(max_length=64)
    portfolio = models.TextField()
