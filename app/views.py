import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from .forms import  *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import json

def home(request):
    return render(request, 'Home/home.html')


def index(request):
    return render(request, 'Site/index.html', {'user': request.user})


def RegisterView(request):


    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email, 
                username=username,
                password=password
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')

    return render(request, 'Authentication/register.html')


def LoginView(request):


    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            return redirect('index')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'Authentication/login.html')

@login_required

def LogoutView(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'Authentication/forgot_password.html')


def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'Authentication/password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=5)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'Authentication/reset_password.html')

# Teacher Registration form starts:
def mystudent_list(request):
    return render(request,'school_app/mystudent_list.html')




def teacher_registration(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debugging step
        
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            try:
                teacher = form.save(commit=False)
                teacher.name = form.cleaned_data['name']
                teacher.phone = form.cleaned_data['phone']
                teacher.email = form.cleaned_data['email']
                teacher.role = form.cleaned_data['role']
                teacher.num_schools = form.cleaned_data['num_schools']
                teacher.save()  # Save the teacher before adding M2M relations
                
                # Save selected schools
                school_ids = request.POST.getlist('school')  # Get multiple school selections
                for school_id in school_ids:
                    try:
                        school = School.objects.get(id=school_id)
                        teacher.schools.add(school)
                    except School.DoesNotExist:
                        print(f"Invalid school ID: {school_id}")

                print(f"Teacher saved successfully with ID: {teacher.id}")
                return redirect('registration_success')
            except Exception as e:
                print(f"Error saving teacher: {str(e)}")
                form.add_error(None, f"Error saving data: {str(e)}")
        else:
            print(f"Form validation errors: {form.errors}")
    else:
        form = TeacherRegistrationForm()

    return render(request, 'school_app/teacher_form.html', {'form': form})


def registration_success(request):
    return render(request, 'school_app/success.html')

# AJAX views for cascading dropdowns
def get_districts(request):
    state_id = request.GET.get('state_id')
    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def get_blocks(request):
    district_id = request.GET.get('district_id')
    blocks = Block.objects.filter(district_id=district_id).values('id', 'name')
    return JsonResponse(list(blocks), safe=False)

def get_schools(request):
    block_id = request.GET.get('block_id')
    schools = School.objects.filter(block_id=block_id).values('id', 'name', 'code')
    return JsonResponse(list(schools), safe=False)

def get_school_code(request):
    school_id = request.GET.get('school_id')
    try:
        school = School.objects.get(id=school_id)
        return JsonResponse({'code': school.code})
    except School.DoesNotExist:
        return JsonResponse({'code': ''})
    

# Here teacher list aa pakkalam ethana school add pannirukanga apd nu pakkalam
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Teacher
from .forms import TeacherRegistrationForm
import json

@login_required
def teacher_list(request):
    teachers = Teacher.objects.filter(user=request.user).prefetch_related("schools__block__district__state")  # Optimized query
    return render(request, 'school_app/teacher_list.html', {'teachers': teachers})

@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id, user=request.user)
    
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherRegistrationForm(instance=teacher)
    
    return render(request, 'school_app/edit_teacher.html', {'form': form})


@require_POST
@login_required
def update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id, user=request.user)

    try:
        data = json.loads(request.body)
        teacher.name = data.get('name', teacher.name)
        teacher.email = data.get('email', teacher.email)
        teacher.num_schools = data.get('num_schools', teacher.num_schools)
        teacher.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@require_POST
@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id, user=request.user)
    
    teacher.delete()
    return JsonResponse({"message": "Teacher deleted successfully!"})

def student_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        # Check if the user has a School_teacher record
        teacher_profile = getattr(request.user, "school_teacher", None)

        if not teacher_profile or not teacher_profile.school_name:
            raise School_teacher.DoesNotExist  # Handle missing school

        students = Record.objects.filter(school_name=teacher_profile.school_name)
        return render(request, 'Student/student_list.html', {'students': students})

    except School_teacher.DoesNotExist:
        contact_email = "admin@gmail.com"
        message = f"Please contact your admin at {contact_email} to assign a school."
        return render(request, 'Student/student_list.html', {'message': message})

def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it =  get_object_or_404(Record, id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('student-list')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('student-list')	

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('front')
		return render(request, 'Student/add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('student-list')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('student-list')
		return render(request, 'Student/update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('student-list')
     

def open_form(request, standard, student_id, subject):
    student = get_object_or_404(Record, id=student_id)

    # Check if the student has already submitted the form for the subject
    already_submitted = FormResponse.objects.filter(student=student, standard=standard, subject=subject).exists()

    if already_submitted:
        return render(request, 'Assessments/form.html', {'student': student, 'form_submitted': True, 'subject': subject})

    # Define questions per subject and grade
    questions_data = {
        6: {
            'Tamil': [
                {'question': 'தமிழ் 1?', 'options': ['விடை 1', 'விடை 2', 'விடை 3', 'விடை 4'], 'correct_answer': 'விடை 2'},
                {'question': 'தமிழ் 2?', 'options': ['விடை 1', 'விடை 2', 'விடை 3', 'விடை 4'], 'correct_answer': 'விடை 3'},
            ],
            'Maths': [
                {'question': 'What is 1 + 10?', 'options': ['9', '10', '11', '12'], 'correct_answer': '11'},
                {'question': 'What is 2 + 3?', 'options': ['4', '5', '6', '7'], 'correct_answer': '5'},
            ],
        },
        7: {
            'Tamil': [
                {'question': 'தமிழ் 1?', 'options': ['விடை 1', 'விடை 2', 'விடை 3', 'விடை 4'], 'correct_answer': 'விடை 1'},
            ],
            'Maths': [
                {'question': 'What is 3 * 3?', 'options': ['6', '7', '8', '9'], 'correct_answer': '9'},
            ],
        }
    }

    questions = questions_data.get(standard, {}).get(subject, [])
    return render(request, 'Assessments/form.html', {'student': student, 'questions': questions, 'form_submitted': False, 'subject': subject})



def submit_form(request, student_id, subject):
    if request.method == 'POST':
        student = get_object_or_404(Record, id=student_id)
        standard = student.standard

        # Check if already submitted
        if FormResponse.objects.filter(student=student, standard=standard, subject=subject).exists():
            return JsonResponse({'error': 'Form already submitted'}, status=400)

        responses = {}
        correct_count = 0

        # Define questions per standard and subject
        questions_data = {
            6: {
                'Tamil': [
                    {'question': 'தமிழ் 1?', 'options': ['விடை 1', 'விடை 2', 'விடை 3', 'விடை 4'], 'correct_answer': 'விடை 2'},
                    {'question': 'தமிழ் 2?', 'options': ['விடை 1', 'விடை 2', 'விடை 3', 'விடை 4'], 'correct_answer': 'விடை 3'},
                ],
                'Maths': [
                    {'question': 'What is 1 + 10?', 'options': ['9', '10', '11', '12'], 'correct_answer': '11'},
                    {'question': 'What is 2 + 3?', 'options': ['4', '5', '6', '7'], 'correct_answer': '5'},
                ],
            },
        }

        questions = questions_data.get(standard, {}).get(subject, [])

        # Process user answers
        for question in questions:
            answer = request.POST.get(f'question_{question["question"]}')
            responses[question["question"]] = answer
            if answer == question['correct_answer']:
                correct_count += 1

        # Save response
        FormResponse.objects.create(
            student=student,
            standard=standard,
            subject=subject,
            responses=responses,
            submitted_at=timezone.now(),
        )

        return redirect('assesment_student_list')

    return JsonResponse({'error': 'Invalid request'}, status=400)

def assesment_student_list(request):
     
    school_name = request.user.school_teacher.school_name
    students = Record.objects.filter(school_name=school_name)

    # Get unique grades
    grades = students.values_list('standard', flat=True).distinct()

    # Get selected grade from request
    selected_grade = request.GET.get('grade', '')

    if selected_grade:
        students = students.filter(standard=selected_grade)

    total_students = students.count()

    # Count submissions for the selected grade
    literacy_submitted = FormResponse.objects.filter(student__in=students, subject='Tamil').count()
    literacy_not_submitted = total_students - literacy_submitted
    numeracy_submitted = FormResponse.objects.filter(student__in=students, subject='Maths').count()
    numeracy_not_submitted = total_students - numeracy_submitted

    # Student-wise submission status
    student_status = {}
    for student in students:
        tamil_submitted = FormResponse.objects.filter(student=student, subject='Tamil').exists()
        maths_submitted = FormResponse.objects.filter(student=student, subject='Maths').exists()
        student_status[student.id] = {
            'tamil_submitted': tamil_submitted,
            'maths_submitted': maths_submitted
        }

    context = {
        'students': students,
        'grades': grades,
        'selected_grade': selected_grade,
        'total_students': total_students,
        'literacy_submitted': literacy_submitted,
        'literacy_not_submitted': literacy_not_submitted,
        'numeracy_submitted': numeracy_submitted,
        'numeracy_not_submitted': numeracy_not_submitted,
        'status': student_status,
    }

    return render(request, 'Assessments/student_list.html', context)
    