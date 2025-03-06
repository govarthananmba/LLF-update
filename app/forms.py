from django import forms
from .models import *

class TeacherRegistrationForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        empty_label="----------",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    district = forms.ModelChoiceField(
        queryset=District.objects.none(),
        empty_label="----------",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    block = forms.ModelChoiceField(
        queryset=Block.objects.none(),
        empty_label="----------",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    school = forms.ModelChoiceField(
        queryset=School.objects.none(),
        empty_label="----------",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    school_code = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'email', 'role', 'num_schools']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'num_schools': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super(TeacherRegistrationForm, self).__init__(*args, **kwargs)
        # If data is posted, filter dependent querysets
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.schools.exists():
            # Pre-populate from the instance’s first school
            school = self.instance.schools.first()
            self.fields['district'].queryset = District.objects.filter(state=school.block.district.state)
            self.initial['district'] = school.block.district

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['block'].queryset = Block.objects.filter(district_id=district_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.schools.exists():
            school = self.instance.schools.first()
            self.fields['block'].queryset = Block.objects.filter(district=school.block.district)
            self.initial['block'] = school.block

        if 'block' in self.data:
            try:
                block_id = int(self.data.get('block'))
                self.fields['school'].queryset = School.objects.filter(block_id=block_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.schools.exists():
            school = self.instance.schools.first()
            self.fields['school'].queryset = School.objects.filter(block=school.block)
            self.initial['school'] = school
            self.initial['school_code'] = school.code

        # If instance exists, also set the state field’s initial value
        if self.instance.pk and self.instance.schools.exists():
            school = self.instance.schools.first()
            self.initial['state'] = school.block.district.state

    def save(self, commit=True, user=None):
        teacher = super().save(commit=False)
        if user:
            teacher.user = user  # Assign the logged-in user
        if commit:
            teacher.save()
            self.save_m2m()  # Save many-to-many relationships
        return teacher

class AddRecordForm(forms.ModelForm):
	funder = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Funder", "class":"form-control"}), label="")
	student_id = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Student ID", "class":"form-control"}), label="")
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
	school_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"School Name", "class":"form-control"}), label="")
	email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
	gender = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Gender", "class":"form-control"}), label="")
	standard= forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Class", "class":"form-control"}), label="")
	section= forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Section", "class":"form-control"}), label="")
	phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
	block = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
	city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
	state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
	

	
    
	class Meta:
		model = Record
		exclude = ("user",)