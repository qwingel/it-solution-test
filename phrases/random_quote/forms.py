from distutils.command.clean import clean

from django import forms
from .models import Source, Quote

class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(max_length=100, label='Название источника')
    source_type = forms.ChoiceField(
        choices=Source.SOURCE_TYPES,
        label="Тип источника",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Quote
        fields = ['text', 'weight', 'source_name', 'source_type']

    def clean(self):
        cleaned_data = super().clean()
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')
        text = cleaned_data.get('text')

        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError('Цитата уже существует')

        source, created = Source.objects.get_or_create(name=source_name, from_where=source_type)
        if Quote.objects.filter(source=source).count() >= 3:
            raise forms.ValidationError("У источника уже 3 цитаты")

        cleaned_data['source'] = source
        return cleaned_data

    def save(self, commit=True):
        quote = super().save(commit=False)
        quote.source = self.cleaned_data['source']
        if commit:
            quote.save()
        return quote