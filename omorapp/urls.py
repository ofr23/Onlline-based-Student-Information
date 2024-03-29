from django.urls import path
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.logIn,name='login'),
    path('catalog/',views.Catalog,name="catalog"),
    path('preclass/',views.preclass,name='preclass'),
    path('class/<int:id>/',views.classes,name='classes'),
    path('class/<int:id>/semester/<int:id2>/',views.semester,name='semester'),
    path('class/<int:id>/semester/<int:id2>/course/<int:id3>/',views.course,name='course'),
    path('teacher/<int:id>',views.teacher,name='teacher'),
    path('evaluate/<int:id>/<int:id2>/<int:id3>/',views.evaluate,name='evaluate'),
    path('result/<int:id>/<int:id2>/',views.result,name='result'),
    path('student/<int:id>/',views.student,name='student'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logg,name='logg'),
    path('hod/<int:id>/',views.hod,name='hod'),
    path('preat/',views.preat,name="preat"),
    path('attendance/<int:id>/<int:id2>/<int:id3>/',views.attendance,name='attendance'),
    path('error/',views.error,name='error'),
    path('er/',views.er,name='er'),
    path('pdf/<str:id>/',views.pdf_view,name='pdf_view'),
    path('search/',views.search,name='search'),

]
