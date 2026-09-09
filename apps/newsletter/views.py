from django.shortcuts import render

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

    send_mail(
        subject='Welcome to NovaGear newsletter!',
        message=(
            'Hello!\n\n'
            'You have successfully subscribed to the NovaGear newsletter.\n\n'
            'We will send you information about new products, '
            'discounts, arrivals, and other updates.\n\n'
            'Sincerely, \n'
            'The NovaGear team'
        ),
        from_email=None,
        recipient_list=[email],
    )

    return JsonResponse({
        'success': True,
        'message': 'You have successfully subscribed! Check your email.'
    })
