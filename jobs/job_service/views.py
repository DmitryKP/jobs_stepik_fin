from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render
from django.views import View
from job_service.models import Company, Specialty, Vacancy


class main_view(View):
    def get(self, request):
        return render(request, 'index.html', context={'specialty': Specialty.objects.all(),
                                                      'company': Company.objects.all()})


class all_vacancies(View):
    def get(self, request):
        return render(request, 'vacancies.html', context={'vacancies': Vacancy.objects.all()})


class spec_vacancies(View):
    def get(self, request, specialization):
        return render(request, 'vacancies_spec.html', context={'vacancies': Vacancy.objects.filter(specialty=specialization).all()})


class one_vacancy(View):
    def get(self, request, vacancy):
        return render(request, 'vacancy.html', context={'vacancies': Vacancy.objects.filter(id=vacancy).all()})


class one_company(View):
    def get(self, request, company):
        return render(request, 'company.html', context={'company': Company.objects.filter(id=company).all(),
                                                        'vacancies': Vacancy.objects.filter(company_id=company).all()})


def custom_handler400(request, exception):
    # Call when SuspiciousOperation raised
    return HttpResponseBadRequest('Неверный запрос!')


def custom_handler403(request, exception):
    # Call when PermissionDenied raised
    return HttpResponseForbidden('Доступ запрещен!')


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
