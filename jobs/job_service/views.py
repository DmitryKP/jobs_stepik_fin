from django.views import View
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
import datetime
from job_service.models import Company, Specialty, Vacancy, Application, Resume
from accounts.forms import UserRegistrationForm, UserLoginForm, ApplicationForm, CompanyForm, VacancyForm, ResumeForm


class main_view(View):
    def get(self, request):
        return render(request, 'index.html', context={'specialty': Specialty.objects.all(),
                                                      'company': Company.objects.all()})


class all_vacancies(View):
    def get(self, request):
        return render(request, 'vacancies.html', context={'vacancies': Vacancy.objects.all()})


class spec_vacancies(View):
    def get(self, request, specialization):
        return render(request, 'vacancies_spec.html',
                      context={'vacancies': Vacancy.objects.filter(specialty=specialization).all()})


class one_vacancy(View):
    def get(self, request, vacancy):
        form = ApplicationForm(request.POST)
        return render(request, 'vacancy.html', context={'vacancies': get_list_or_404(Vacancy, id=vacancy),
                                                        'appl_form': form})

    def post(self, request, vacancy):
        form = ApplicationForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            print('ok')
            new_appl = Application.objects.create(
                user_id=request.user.id,
                vacancy_id=vacancy,
                written_username=form.cleaned_data["written_username"],
                written_phone=form.cleaned_data["written_phone"],
                written_cover_letter=form.cleaned_data["written_cover_letter"]
            )
            new_appl.save()
            return redirect("vac_send", vacancy=vacancy)
        else:
            return render(request, 'vacancy.html', context={'appl_form': form,
                                                            'vacancies': Vacancy.objects.filter(id=vacancy).all(),
                                                            'error_message': 'Заполните все поля для отправки формы'})


class one_vacancy_send(View):
    def get(self, request, vacancy):
        return render(request, 'vacancy-app-send.html', context={'vac_id': vacancy})


class one_company(View):
    def get(self, request, company):
        return render(request, 'company.html', context={'company': Company.objects.filter(id=company).all(),
                                                        'vacancies': Vacancy.objects.filter(company_id=company).all()})


# LK funcs
@method_decorator(login_required(login_url='/login'), name='dispatch')
class start_create_company(View):
    def get(self, request):
        if Company.objects.filter(owner_id=request.user.id).all():
            return redirect('edit_company')
        else:
            return render(request, 'company-letsstart.html', context={})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class create_company(View):
    def get(self, request):
        if Company.objects.filter(owner_id=request.user.id).all():
            return HttpResponseNotFound('У вас уже есть компания')
        else:
            form = CompanyForm()
            return render(request, 'company-create.html', context={'c_form': form})

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if request.user.is_authenticated and form.is_valid():
            new_c = Company.objects.create(
                owner_id=request.user.id,
                name=form.cleaned_data["name"],
                location=form.cleaned_data["location"],
                description=form.cleaned_data["description"],
                employee_count=form.cleaned_data["employee_count"],
                logo=form.cleaned_data["logo"]
            )

            new_c.save()
            messages.success(request, 'Компания создана. Отредактируйте ее здесь')
            return redirect('edit_company')
        else:
            return render(request, 'company-create.html', context={'c_form': form,
                                                                   'error_message': 'Заполните все поля корректно для отправки формы'})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class edit_company(View):
    def get(self, request):
        cdata_user = get_object_or_404(Company, owner_id=request.user.id)
        form = CompanyForm(initial={'name': cdata_user.name,
                                    'location': cdata_user.location,
                                    'description': cdata_user.description,
                                    'employee_count': cdata_user.employee_count,
                                    'logo': cdata_user.logo})
        return render(request, 'company-edit.html', context={'c_form': form})

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if request.user.is_authenticated and form.is_valid():
            Company.objects.filter(owner_id=request.user.id).update(
                name=form.cleaned_data["name"],
                location=form.cleaned_data["location"],
                description=form.cleaned_data["description"],
                employee_count=form.cleaned_data["employee_count"],
                logo=form.cleaned_data["logo"]
            )

            messages.success(request, 'Данные вашей компании изменены')
        else:
            return render(request, 'company-edit.html', context={'c_form': form, 'error_message': 'Залогиньтесь и заполните все поля для отправки формы'})
        return render(request, 'company-edit.html', context={'c_form': form})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class list_vacancy(View):
    def get(self, request):
        company_user_id = get_object_or_404(Company, owner_id=request.user.id).id
        return render(request, 'vacancy-list.html', context={
                                             'vacs': Vacancy.objects.filter(company_id=company_user_id).all()})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class create_vacancy(View):
    def get(self, request):
        form = VacancyForm()
        return render(request, 'vacancy-create.html', context={'v_form': form})

    def post(self, request):
        form = VacancyForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            new_v = Vacancy.objects.create(
                title=form.cleaned_data["title"],
                salary_min=form.cleaned_data["salary_min"],
                salary_max=form.cleaned_data["salary_max"],
                specialty=form.cleaned_data["specialty"],
                skills=form.cleaned_data["skills"],
                description=form.cleaned_data["description"],
                company=Company.objects.get(owner_id=request.user.id),
                published_at=datetime.date.today().strftime("%Y-%m-%d")
            )

            new_v.save()
            messages.success(request, 'Вакансия создана. Отредактируйте ее здесь')
            return redirect("edit_vacancy", vacancy=new_v.id)
        else:
            return render(request, 'vacancy-create.html', context={'v_form': form,
                                                                   'error_message': 'Залогиньтесь и заполните и заполните все поля для отправки формы'})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class edit_vacancy(View):
    def get(self, request, vacancy):
        if Company.objects.filter(owner_id=request.user.id).first().id == Vacancy.objects.filter(id=vacancy).first().company_id:
            vdata = get_object_or_404(Vacancy, id=vacancy)
            form = VacancyForm(initial={'title': vdata.title,
                                        'salary_min': vdata.salary_min,
                                        'salary_max': vdata.salary_max,
                                        'specialty': vdata.specialty,
                                        'skills': vdata.skills,
                                        'description': vdata.description
                                        })

            a_data = Application.objects.filter(vacancy=vacancy).all()

            return render(request, 'vacancy-edit.html', context={'v_form': form, 'a_data': a_data})
        else:
            return HttpResponseNotFound('Это не ваша вакансия')

    def post(self, request, vacancy):
        form = VacancyForm(request.POST)
        a_data = Application.objects.filter(vacancy=vacancy).all()
        if request.user.is_authenticated and form.is_valid():
            Vacancy.objects.filter(id=vacancy).update(
                title=form.cleaned_data["title"],
                salary_min=form.cleaned_data["salary_min"],
                salary_max=form.cleaned_data["salary_max"],
                specialty=form.cleaned_data["specialty"],
                skills=form.cleaned_data["skills"],
                description=form.cleaned_data["description"],
                company=Company.objects.get(owner_id=request.user.id),
                published_at=datetime.date.today().strftime("%Y-%m-%d")
            )

            messages.success(request, 'Вакансия отредактирована')
        else:
            return render(request, 'vacancy-edit.html', context={'v_form': form,
                                                                 'a_data': a_data,
                                                                 'error_message': 'Залогиньтесь и заполните и заполните все поля для отправки формы'})
        return render(request, 'vacancy-edit.html', context={'v_form': form,
                                                             'a_data': a_data})


# Authorize funcs
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main')
        else:
            form = UserRegistrationForm()
            return render(request, 'register.html', context={'r_form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            login(request, new_user)
            return redirect('main')
        else:
            return render(request, 'register.html', context={'r_form': form,
                                                             'error_message': 'Форма заполнена некорректно'})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main')
        else:
            form = UserLoginForm()
            return render(request, 'login.html', context={'u_form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("main")
            else:
                return render(request, 'login.html', {'u_form': form,
                                                      'error_message': 'Авторизация не успешна. Попробуйте еще раз'})


# LK Resume

class search_vacancies(View):

    def get(self, request):
        query = self.request.GET.get('s')
        print(query)
        search_res = Vacancy.objects.filter(
           Q(title__icontains=query) | Q(description__icontains=query)
        ).all()
        return render(request, 'search.html', context={'s_list': search_res})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class start_create_resume(View):
    def get(self, request):
        if Resume.objects.filter(user_id=request.user.id).all():
            return redirect('edit_resume')
        else:
            return render(request, 'resume-letsstart.html', context={})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class create_resume(View):
    def get(self, request):
        if Resume.objects.filter(user_id=request.user.id).all():
            return HttpResponseNotFound('У вас уже есть одно резюме')
        else:
            form = ResumeForm()
            return render(request, 'resume-create.html', context={'r_form': form})

    def post(self, request):
        form = ResumeForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            new_r = Resume.objects.create(
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                status=form.cleaned_data["status"],
                salary=form.cleaned_data["salary"],
                specialty=form.cleaned_data["specialty"],
                education=form.cleaned_data["education"],
                experience=form.cleaned_data["experience"],
                grade=form.cleaned_data["grade"],
                portfolio=form.cleaned_data["portfolio"],
                user_id=request.user.id
            )

            new_r.save()
            messages.success(request, 'Резюме создано. Отредактируйте его здесь')
            return redirect('edit_resume')
        else:
            return render(request, 'resume-create.html', context={'r_form': form,
                                                                  'error_message': 'Залогиньтесь и заполните и заполните все поля для отправки формы'})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class edit_resume(View):
    def get(self, request):
        rdata_user = get_object_or_404(Resume, user_id=request.user.id)
        form = ResumeForm(initial={'name': rdata_user.name,
                                   'surname': rdata_user.surname,
                                   'status': rdata_user.status,
                                   'salary': rdata_user.salary,
                                   'specialty': rdata_user.specialty,
                                   'education': rdata_user.education,
                                   'experience': rdata_user.experience,
                                   'grade': rdata_user.grade,
                                   'portfolio': rdata_user.portfolio})
        return render(request, 'resume-edit.html', context={'r_form': form})

    def post(self, request):
        form = ResumeForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            Resume.objects.filter(user_id=request.user.id).update(
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                status=form.cleaned_data["status"],
                salary=form.cleaned_data["salary"],
                specialty=form.cleaned_data["specialty"],
                education=form.cleaned_data["education"],
                experience=form.cleaned_data["experience"],
                grade=form.cleaned_data["grade"],
                portfolio=form.cleaned_data["portfolio"],
                user_id=request.user.id
            )

            messages.success(request, 'Ваше резюме изменено')
        else:
            return render(request, 'resume-edit.html', context={'r_form': form, 'error_message': 'Залогиньтесь и заполните все поля для отправки формы'})
        return render(request, 'resume-edit.html', context={'r_form': form})


# Handlers
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
