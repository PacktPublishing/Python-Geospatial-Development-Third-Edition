from django import forms

class ImportShapefileForm(forms.Form):
  import_file = forms.FileField(label="Select a Zipped Shapefile")

