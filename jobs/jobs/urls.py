"""jobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


from job_service.views import main_view, all_vacancies, spec_vacancies, one_vacancy, one_company, \
     custom_handler400, custom_handler403, custom_handler404, custom_handler500, \
     start_create_company, create_company, edit_company, \
     list_vacancy, create_vacancy, edit_vacancy, one_vacancy_send, \
     RegisterView, LoginView

urlpatterns = [
    path('', main_view.as_view(), name="main"),
    path('vacancies/', all_vacancies.as_view()),
    path('vacancies/cat/<str:specialization>', spec_vacancies.as_view()),
    path('vacancies/<int:vacancy>', one_vacancy.as_view(), name="vac"),
    path('vacancies/<int:vacancy>/send/', one_vacancy_send.as_view(), name="vac_send"),
    path('companies/<int:company>', one_company.as_view()),
    path('mycompany/letsstart/', start_create_company.as_view()),
    path('mycompany/create/', create_company.as_view(), name="create_company"),
    path('mycompany/', edit_company.as_view(), name="edit_company"),
    path('mycompany/vacancies/', list_vacancy.as_view()),
    path('mycompany/vacancies/create/', create_vacancy.as_view()),
    path('mycompany/vacancies/<int:vacancy>/', edit_vacancy.as_view()),
    path('admin/', admin.site.urls),
    path('register/', RegisterView, name="registration"),
    path('login/', LoginView,  name="auth"),
    path('logout/', LogoutView.as_view())

]

handler400 = custom_handler400
handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
