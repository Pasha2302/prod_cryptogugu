# views.py
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
import sendgrid
# from sendgrid.helpers.mail import Mail
from django.conf import settings


def subscribe(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        agree = request.POST.get('agree')

        if not email or not agree:
            messages.error(request, "Please provide a valid email and agree to the terms.")
            return redirect('index')  # Замените 'home' на имя вашей главной страницы

        try:
            # Отправка данных в SendGrid
            sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            list_id = settings.SENDGRID_LIST_ID

            data = {
                "list_ids": [list_id],
                "contacts": [{"email": email}]
            }

            response = sg.client.marketing.contacts.put(request_body=data)
            if response.status_code == 202:
                messages.success(request, "You have successfully subscribed!")
            else:
                messages.error(request, "Failed to subscribe. Please try again later.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('index')  # Замените 'home' на имя вашей главной страницы

    # return render(request, 'your_template.html')  # Замените 'your_template.html' на имя вашего шаблона

