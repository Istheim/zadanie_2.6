from builtins import super

from django import forms

from catalog.models import Product, Version, Category


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_current_version":
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'  # Все поля
        # fields = ('name_prod', 'description_prod', 'img_prod')
        exclude = ('user_boss',)  # поля которые исключаются

    def clean_name_prod(self):
        cleaned_data = self.cleaned_data['name_prod']

        if cleaned_data.title() in ['Казино', 'Криптовалюта', 'Крипта', 'Биржа', 'Дешево', 'Бесплатно', 'Обман',
                                    'Полиция',
                                    'Радар']:
            raise forms.ValidationError('Ой, всё, запрещенное слово')

        return cleaned_data

    def clean_description_prod(self):
        cleaned_data = self.cleaned_data['description_prod']

        if cleaned_data.title() in ['Казино', 'Криптовалюта', 'Крипта', 'Биржа', 'Дешево', 'Бесплатно', 'Обман',
                                    'Полиция',
                                    'Радар']:
            raise forms.ValidationError('Ой, всё, запрещенное слово')

        return cleaned_data


class ProductsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'category', 'price', 'is_active')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)

        # Проверяем, является ли пользователь модератором
        if not self.user_has_moderator_permission(user):
            self.fields['title'].widget.attrs['readonly'] = True
            self.fields['description'].widget.attrs['readonly'] = True
            self.fields['is_active'].widget.attrs['readonly'] = True

    def user_has_moderator_permission(self, user):
        if user and user.has_perm('catalog.change_product'):
            return True
        return False


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
        # fields = ('name_prod', 'description_prod', 'img_prod')
        # exclude = () # поля которые исключаются


class CategoryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
