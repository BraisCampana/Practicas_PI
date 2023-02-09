from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class RegisterForm(forms.Form, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-registerForm'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_action = 'register_error_view'
        self.helper.add_input(Submit('registrar', 'Registrarse'))

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                 Submit('login', 'Login', css_class='btn-primary')
            )
        )

#class SignupForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        super(SignupForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper(self)
#        self.helper.form_method = 'POST'
#        self.helper.form_action = reverse_lazy('index')
#        self.helper.add_input(Submit('registrar', 'Registrarse'))

#    country=forms.ChoiceField(
#        choices=User.Countries.choices
#    )
#    date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date()}))
#    email=forms.CharField()

#    class Meta:
#        fields = ('username','password','country','date','email')
#        widgets = {
#            'password': forms.PasswordInput()
#        }
