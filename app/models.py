from django.db import models
from django.contrib.auth.models import User
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"



class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'state')
    
    def __str__(self):
        return self.name

class Block(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'district')
    
    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'block')
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    role = models.CharField(max_length=15)
    num_schools = models.PositiveIntegerField(verbose_name="Number of Schools")
    schools = models.ManyToManyField(School)

    def __str__(self):
        return self.name
    

class Record(models.Model):
	student_id = models.CharField(max_length=50,unique=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	school_name =  models.CharField(max_length=100)
	email =  models.CharField(max_length=100)
	gender=models.CharField(max_length=10)
	standard=models.IntegerField()
	section=models.CharField(max_length=10)
	phone = models.CharField(max_length=15)
	block =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	funder =models.CharField(max_length=50)
	

	def __str__(self):
		
		return(f"{self.student_id} {self.first_name} {self.last_name} {self.school_name}")


class School_teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100, default="Unknown School")  # Set a default value

    def __str__(self):
        return f"{self.user.username} - {self.school_name}"


    


    
class QuestionBank(models.Model):
    standard = models.IntegerField()
    question_text = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Standard {self.standard}: {self.question_text[:50]}..."

class FormResponse(models.Model):
    student = models.ForeignKey(Record, on_delete=models.CASCADE)
    standard = models.IntegerField()
    subject = models.CharField(max_length=10, choices=[('Tamil', 'Tamil'), ('Maths', 'Maths')])  # Track subject
    responses = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    assessment_status = models.CharField(max_length=50, default="Not Assessed")

    class Meta:
        unique_together = ('student', 'standard', 'subject')  # Ensure one submission per subject
