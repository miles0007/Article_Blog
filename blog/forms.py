from blog.models import Post,Comment
from django import forms
class EmailForm(forms.Form):
	name = forms.CharField(max_length=50)
	email = forms.EmailField()
	to = forms.EmailField()
	subject = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','email','body')

class SearchForm(forms.Form):
	query = forms.CharField()