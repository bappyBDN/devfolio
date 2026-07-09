
from django.shortcuts import render
from django.contrib import messages
from .models import Message

def contact_view(request):
    """
    Handles displaying the contact form and processing submissions.
    """
    context = {}
    
    if request.method == 'POST':
        sender_name = request.POST.get('sender_name')
        sender_email = request.POST.get('sender_email')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')

        # Basic validation
        if sender_name and sender_email and message_body:
            try:
                # Create and save the new message
                Message.objects.create(
                    sender_name=sender_name,
                    sender_email=sender_email,
                    subject=subject,
                    message=message_body
                )
                context['form_success'] = True
            except Exception as e:
                context['form_error'] = "An error occurred while sending your message. Please try again later."
        else:
            context['form_error'] = "Please fill in all required fields."

    return render(request, 'pages/contact.html', context)