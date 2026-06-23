from django import forms


class ConfirmEmail(forms.Form):
    confirm_code = forms.CharField(
        max_length=6,
        error_messages={
            "required": "Введіть код підтвердження",
        }
    )