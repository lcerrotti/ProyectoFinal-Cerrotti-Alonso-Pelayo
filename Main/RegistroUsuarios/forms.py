from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from RegistroUsuarios.models import Avatar

username_validator = UnicodeUsernameValidator()

# Formulario de Registro , establecemos los Placeholders, caracteres y formato

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_('.'),max_length=12, min_length=4, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre'}))
    last_name = forms.CharField(label=_('.'),max_length=12, min_length=4, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control','placeholder':'Apellido'})))
    email = forms.EmailField(label=_('.'),max_length=50,
                             widget=(forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'})))
    password1 = forms.CharField(label=_('.'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Contraseña'})),
                                help_text=_('Al menos 8 caracteres alfanumericos'))
    password2 = forms.CharField(label=_('.'), widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Repetir Contraseña'}),
                                help_text=_('Ingresa de nuevo tu contraseña para Confirmar'))
    username = forms.CharField(
        label=_('.'),
        max_length=150,
        help_text=_(''),
        validators=[username_validator],
        error_messages={'unique': _("El nombre de usuario ingresado ya existe")},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Usuario'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        

# Formulario de Edicion de perfil , establecemos los Placeholders, caracteres y formato
class UserEditForm(UserChangeForm):

    password = forms.CharField(
        help_text="",
        widget=forms.HiddenInput(), required=False
    )

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','username']
        widgets= {
            'imagen': forms.FileInput(
                attrs={
                    'type': 'file',
                    'class': 'form-control',
                
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'type': 'email',
                    'class': 'form-control',
                    'placeholder': 'Email',
                    'required': 'true',
                    'data-sb-validations':'required|email',
                    'data-sb-errors':'Email no válido',
                    'data-sb-required-message':'Email requerido',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                    'required': 'true',
                    'data-sb-validations':'required',
                    'data-sb-errors':'Nombre requerido',
                    'data-sb-required-message':'Nombre requerido',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Apellido',
                    'required': 'true',
                    'data-sb-validations':'required',
                    'data-sb-errors':'Apellido requerido',
                    'data-sb-required-message':'Apellido requerido',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Nombre de usuario',
                    'required': 'true',
                    'data-sb-validations':'required',
                    'data-sb-errors':'Nombre de usuario requerido',
                    'data-sb-required-message':'Nombre de usuario requerido',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'type': 'password',
                    'class': 'form-control',
                    'placeholder': 'Contraseña',
                    'required': 'true',
                    'data-sb-validations':'required',
                    'data-sb-errors':'Contraseña requerida',
                    'data-sb-required-message':'Contraseña requerida',
                }
            ),
            
        }

    def clean_password2(self):

        password2 = self.cleaned_data["password2"]
        if password2 != self.cleaned_data["password1"] or password2.isnumeric() or len(password2) < 8:
            raise forms.ValidationError("...")
            
        return password2


# Traemos el formulario de Avatar para renderizarlo con formato en la web.
class AvatarFormulario(forms.ModelForm):

    class Meta:
        model=Avatar
        fields=('imagen',) 
        widgets= {
            'imagen': forms.FileInput(
                attrs={
                    'type': 'file',
                    'class': 'form-control',
                
                }
            ),
        }