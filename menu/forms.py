from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(label='名前', widget=forms.TextInput(attrs={'class':'form-control django-form'}))
    email = forms.EmailField(label='メール', widget=forms.TextInput(attrs={'class':'form-control django-form'}))
    enter_password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class':'form-control django-form'}))
    retype_password = forms.CharField(label='パスワード(確認)', widget=forms.PasswordInput(attrs={'class':'form-control django-form'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('このユーザー名はすでに使われています。')
        return username

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 5:
            raise forms.ValidationError('パスワードは５文字以上で入力してください。')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error('retype_password', 'パスワードが一致しません。')

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        email = self.cleaned_data.get('email')
        new_user = User.objects.create_user(username = username)
        new_user.set_password(password)
        new_user.save()



