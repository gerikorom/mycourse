from django import forms
from .models import *
from .validators import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FelvetelForm(forms.Form):
    cim = forms.CharField(error_messages={'required': 'Kérjük adja meg!'})
    iro = forms.CharField()
    leiras = forms.CharField(label='Leírás',
                             required=False,
                             widget=forms.Textarea(
                                 attrs={
                                     "class":"form-control",
                                     "rows":3,
                                     "id":"leiras-id"
                                 }
                             )
                             )
    ar = forms.IntegerField()
    elerheto = forms.BooleanField()

class SajatModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} {}".format(obj.iro, obj.cim)

class KolcsonzesForm(forms.ModelForm):
    konyv = SajatModelChoiceField(queryset=Konyv.objects.all(),label='Válasszon könyvet előjegyzéshez!')

    class Meta:
        model = Kolcsonzes
        fields = ['konyv']

class ResztvetelSajatModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} {}".format(obj.elnevezes, obj.idopont.strftime('%Y.%m.%d'))

class ResztvetelForm(forms.ModelForm):
    olvasoest = ResztvetelSajatModelChoiceField(queryset=OlvasoEst.objects.filter(helyekszama__gt=0),label='Válassza ki az olvasóestet!')

    class Meta:
        model = Resztvetel
        fields = ['olvasoest']

class KonyvForm(forms.ModelForm):
    class Meta:
        model = Konyv
        fields = [
            'cim',
            'iro',
            'leiras',
            'ar',
            'elerheto'
        ]
        #fields = '__all__'
        '''
        widgets = {
            "cim": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder":'Cím'
                }
            )
        }
        '''
        labels = {
            "cim": "Cím"
        }


    def clean_cim(self):
        cim = self.cleaned_data.get('cim')
        if not 'Harry Potter' in cim:
            raise forms.ValidationError('Harry Potter könyvet adjon meg!')
        else:
            return cim

    def clean_ar(self):
        ar = self.cleaned_data.get('ar')
        if 10000 < ar:
            raise forms.ValidationError('Könyv túl drága')
        else:
            return ar

hibauzenetek = {
    'required': 'Kötelező feltölteni!',
    'invalid': 'Hiba!'
}

class ExcelFeltoltesForm(forms.Form):
    file = forms.FileField(label='Feltöltés',
                           error_messages=hibauzenetek,
                           validators=[excel_validator])

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcionális.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcionális.')
    email = forms.EmailField(max_length=254, help_text='Szükséges.')
    password2 = forms.CharField(label='Jelszó mégegyszer', widget=forms.PasswordInput, help_text=None)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )









