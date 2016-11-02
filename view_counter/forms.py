from view_counter.models import Posted_Sale
from django.contrib.auth.models import User
from django import forms



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'password')
		

class Posted_SaleForm(forms.ModelForm):
	Sale_title = forms.CharField(label = 'Title')
	Sale_descript = forms.CharField( label = 'Description')
	class Meta:
		model = Posted_Sale;
		exclude = ['user']