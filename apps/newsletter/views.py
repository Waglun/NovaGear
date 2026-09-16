from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import NewsletterSubscriber


@require_POST
def subscribe(request):
    email = request.POST.get('email', '').strip()

    if not email:
        return JsonResponse({
            'success': False,
            'message': 'Введите email.'
        }, status=400)

    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={'is_active': True},
    )

    if not created and subscriber.is_active:
        return JsonResponse({
            'success': False,
            'message': 'Этот email уже подписан на рассылку.'
        })

    if not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save(update_fields=['is_active'])

    html_message = render_to_string(
        'welcome_email.html',
        {
            'email': email,
        }
    )

    email_message = EmailMultiAlternatives(
        subject='Welcome to NovaGear newsletter!',
        body=(
            'Здравствуйте!\n\n'
            'Вы успешно подписались на рассылку NovaGear.\n\n'
            'С уважением,\n'
            'Команда NovaGear'
        ),
        from_email=None,
        to=[email],
    )

    email_message.attach_alternative(
        html_message,
        'text/html',
    )

    email_message.send()

    return JsonResponse({
        'success': True,
        'message': 'You have successfully subscribed! Check your email.'
    })
