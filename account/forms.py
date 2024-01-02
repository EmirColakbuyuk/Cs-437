from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserProfileForm(UserChangeForm):
    password = None  # Bu satır, formda password alanını tamamen kaldırır.

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # exclude = ('password',) # Bu satırı kaldırdık çünkü zaten 'fields' ile hangi alanların kullanılacağını belirttik.

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # Kullanıcı adı için yardımcı metni kaldırır.
        self.fields['email'].help_text = None     # E-posta için yardımcı metni kaldırır.
        # Diğer alanlar için de benzeri işlemler uygulanabilir.
