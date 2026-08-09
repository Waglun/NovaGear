from django import forms


class OrderForm(forms.Form):
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Введите адрес доставки',
        }),
    )

    phone = forms.CharField(
        label='Телефон',
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
        }),
    )

    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Комментарий к заказу',
        }),
    )