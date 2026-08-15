from django import forms


class OrderForm(forms.Form):
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Введите адрес доставки',
            'class': 'input input--textarea',
        }),
    )

    phone = forms.CharField(
        label='Телефон',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '+7 (999) 123-45-67',
        }),
    )

    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input input--textarea',
            'rows': 3,
            'placeholder': 'Комментарий к заказу',
        }),
    )