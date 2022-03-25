from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from job_service.models import Application, Company, Vacancy, Resume
from django.forms import ModelForm
from crispy_forms.helper import FormHelper


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['email'].label = "Электронная почта"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    model = User
    fields = ['username', 'password']


class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count', 'logo')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Название"
        self.fields['location'].label = "Локация"
        self.fields['description'].label = "Описание"
        self.fields['employee_count'].label = "Кол-во работников"
        self.fields['logo'].label = "Логотип"

        self.helper = FormHelper()
        self.helper.form_tag = False


class VacancyForm(ModelForm):

    class Meta:
        model = Vacancy
        fields = ('title', 'salary_min', 'salary_max', 'specialty', 'skills', 'description')

    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название вакансии"
        self.fields['skills'].label = "Требуемые навыки"
        self.fields['salary_min'].label = "Зарплата от"
        self.fields['salary_max'].label = "Зарплата до"
        self.fields['specialty'].label = "Специализация"

        self.helper = FormHelper()
        self.helper.form_tag = False


class ResumeForm(ModelForm):

    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary', 'specialty', 'education', 'experience', 'grade', 'portfolio')

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Ваше имя"
        self.fields['surname'].label = "Ваше фамилия"
        self.fields['status'].label = "Статус поиска"
        self.fields['salary'].label = "Желаемая зарплата"
        self.fields['specialty'].label = "Специальность"
        self.fields['education'].label = "Образование"
        self.fields['experience'].label = "Опыт"
        self.fields['grade'].label = "Уровень"
        self.fields['portfolio'].label = "Портфолио"

        self.helper = FormHelper()
        self.helper.form_tag = False
