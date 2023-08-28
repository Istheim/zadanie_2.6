from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('name_prod', 'description_prod', 'img_prod')
        # exclude = () # поля которые исключаются

    def clean_name_prod(self):
        cleaned_data = self.cleaned_data['name_prod']

        if cleaned_data in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                            'радар']:
            raise forms.ValidationError('Ой, всё, запрещенное слово')

        return cleaned_data

    def clean_description_prod(self):
        cleaned_data = self.cleaned_data['description_prod']

        if cleaned_data in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                            'радар']:
            raise forms.ValidationError('Ой, всё, запрещенное слово')

        return cleaned_data
