from django import forms

class JSONUploadForm(forms.Form):
    json_file = forms.FileField(label="Upload JSON file")
