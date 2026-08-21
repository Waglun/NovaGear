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


class PaymentForm(forms.Form):
    card_name = forms.CharField(
        label='Имя карты',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': "IVAN IVANOV",
            'style': 'text-transform: uppercase',
        })
    )

    card_number = forms.CharField(
        label='Номер карты',
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': "1234 5678 9012 3456",

        })
    )

    card_expiry = forms.CharField(
        label='Срок действия',
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': "MM/YY",
        })
    )

    card_cvv = forms.CharField(
        label= 'CVV',
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': "123",
        })
    )






