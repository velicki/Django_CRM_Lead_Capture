from django import forms
from django.forms import ModelForm
from .models import Topic, About, Lead

class LeadForm(ModelForm):

    class Meta:
        model = Lead
        fields = ['topic', 'name', 'email', 'phone', 'description']
    
    def __init__(self, *args, user=None,**kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        # Filter the topics based on the user
        self.fields['topic'].queryset = Topic.objects.filter(user=user)

class TopicForm(ModelForm):

    class Meta:
        model = Topic
        fields = ['name']

class AboutForm(ModelForm):

    class Meta:
        model = About
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super(AboutForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={
            'id': 'myTextarea'})

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')