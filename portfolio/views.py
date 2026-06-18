from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from mailjet_rest import Client

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def send_contact_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            
            # Configuration Mailjet
            mailjet = Client(
                auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET),
                version='v3.1'
            )

            # Envoi de l'email à moi-même
            admin_email_data = {
                'Messages': [
                    {
                        "From": {
                            "Email": settings.DEFAULT_FROM_EMAIL,
                            "Name": "Portfolio Uyen"
                        },
                        "To": [
                            {
                                "Email": settings.CONTACT_EMAIL,
                                "Name": "Thanh Uyen Nguyen"
                            }
                        ],
                        "Subject": f"[Portfolio] {subject} - de {name}",
                        "TextPart": f"""
                            Nom: {name}
                            Email: {email}
                            Sujet: {subject}

                            Message:
                            {message}
                            """,
                            "HTMLPart": f"""
                            <h3>Nouveau message depuis mon portfolio</h3>
                            <p><strong>Nom:</strong> {name}</p>
                            <p><strong>Email:</strong> {email}</p>
                            <p><strong>Sujet:</strong> {subject}</p>
                            <p><strong>Message:</strong></p>
                            <p>{message}</p>
                        """,
                    }
                ]
            }
            
            result = mailjet.send.create(data=admin_email_data)
            
            if result.status_code == 200:
                # Email de confirmation à l'expéditeur
                confirmation_data = {
                    'Messages': [
                        {
                            "From": {
                                "Email": settings.DEFAULT_FROM_EMAIL,
                                "Name": "Thanh Uyen Nguyen"
                            },
                            "To": [
                                {
                                    "Email": email,
                                    "Name": name
                                }
                            ],
                            "Subject": "Confirmation de réception de votre message",
                            "TextPart": f"""
                                Bonjour {name},

                                Je vous remercie pour votre message. Je vous répondrai dans les plus brefs délais.

                                Cordialement,
                                Thanh Uyen Nguyen
                                """,
                                "HTMLPart": f"""
                                <h3>Bonjour {name},</h3>
                                <p>Je vous remercie pour votre message. Je vous répondrai dans les plus brefs délais.</p>
                                <br>
                                <p>Cordialement,<br>
                                <strong>Thanh Uyen Nguyen</strong></p>
                            """,
                        }
                    ]
                }
                mailjet.send.create(data=confirmation_data)
                
                return JsonResponse({'success': True, 'message': 'Message envoyé avec succès ! Je vous répondrai rapidement.'})
            else:
                return JsonResponse({'success': False, 'message': 'Erreur lors de l\'envoi du message. Veuillez réessayer.'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur : {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})