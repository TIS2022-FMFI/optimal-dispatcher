from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
  
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['new_password1'].help_text=''