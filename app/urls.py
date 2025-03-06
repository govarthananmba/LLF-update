from django.urls import path
from .import views
urlpatterns = [  
    
    path('',views.home, name= 'home'),
    path('index/', views.index, name='index'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),

    path('mystudent_list/', views.mystudent_list, name='mystudent_list'),
    path('teacher_registration/', views.teacher_registration, name='teacher_registration'), 
    path('success/', views.registration_success, name='registration_success'),
    path('ajax/districts/', views.get_districts, name='ajax_districts'),
    path('ajax/blocks/', views.get_blocks, name='ajax_blocks'),
    path('ajax/schools/', views.get_schools, name='ajax_schools'),
    path('ajax/school-code/', views.get_school_code, name='ajax_school_code'),

    path('teacher_list/', views.teacher_list, name='teacher_list'),
    path('edit-teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('update-teacher/<int:teacher_id>/', views.update_teacher, name='update_teacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('students/', views.student_list, name='student-list'),

    path('form/<int:standard>/<int:student_id>/<str:subject>/', views.open_form, name='open_form'),
    path('submit_form/<int:student_id>/<str:subject>/', views.submit_form, name='submit_form'),
    path('assesment_student_list/', views.assesment_student_list, name='assesment_student_list'),

]