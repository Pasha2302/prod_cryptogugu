import re
import sendgrid
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest


def validate_subscription_data(email, agree) -> dict:
    errors = {}

    # Валидация email
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        errors['email'] = 'Invalid email address'

    # Валидация согласия
    if not agree:
        errors['agree'] = 'You must agree to the terms'

    return errors


def handle_subscription(email):
    """Обработка подписки через SendGrid."""
    try:
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        list_id = settings.SENDGRID_LIST_ID
        data = {
            "list_ids": [list_id],
            "contacts": [{"email": email}]
        }
        response = sg.client.marketing.contacts.put(request_body=data)

        if response.status_code == 202:
            return 'You have successfully subscribed!', None
        else:
            return None, 'Subscription failed, please try again later.'

    except Exception as e:
        return None, f'Error: {str(e)}'


def subscribe(request: HttpRequest):
    template_name = 'app/components_html/mail_subscribe/subscribe.html'

    email = request.POST.get('email', '')
    agree = request.POST.get('agree', False)

    # Создание начального контекста
    context = {
        'email': email,
        'agree': agree
    }

    # Валидация данных
    errors = validate_subscription_data(email, agree)
    if errors:
        context['errors'] = errors
        return render(request, template_name, context)

    # Обработка подписки
    success, error_message = handle_subscription(email)
    if error_message:
        context['errors'] = {'general': error_message}
        return render(request, template_name, context)

    # Успешная подписка
    context['success'] = success
    return render(request, template_name, context)
