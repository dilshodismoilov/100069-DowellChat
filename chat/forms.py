from django import forms
from .models import CsvUpload
    
    
class UploadFileForm(forms.ModelForm):

    class Meta:
        model = CsvUpload
        fields = ('file_name',)