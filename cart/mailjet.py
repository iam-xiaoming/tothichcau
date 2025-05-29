from mailjet_rest import Client
from blog.models import EmailSubscription
from django.conf import settings

api_key = settings.MAILJET_API_KEY
api_secret = settings.MAILJET_API_SECRET
sender = settings.SENDER

from mailjet_rest import Client

def send_mailjet_email_new_game_announcement(game_name, game_description, game_release_date, game_url):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    # lấy tất cả các subscriptor đăng ký và gửi thông báo về tựa game mới ra mắt
    emails = EmailSubscription.objects.all()
    for email in emails:
        data = {
            "Messages": [
                {
                    "From": {
                        "Email": sender,
                        "Name": "Game Art"
                    },
                    "To": [
                        {
                            "Email": email.email,
                            "Name": "Subscriber"
                        }
                    ],
                    "Subject": f"🔥 New Game Alert: {game_name} is now available!",
                    "TextPart": (
                        f"Hey gamer!\n\n"
                        f"We've just added a new game to our store:\n\n"
                        f"Title: {game_name}\n"
                        f"Release Date: {game_release_date}\n"
                        f"Description: {game_description}\n\n"
                        f"Check it out now: {game_url}"
                    ),
                    "HTMLPart": f"""
                        <div style="font-family: Arial, sans-serif; color: #333;">
                            <h2 style="color: #e63946;">🚨 New Game Just Dropped!</h2>
                            <p>We're thrilled to announce a brand-new addition to our collection:</p>
                            <h3 style="color: #1d3557;">🎮 {game_name}</h3>
                            <p><strong>🗓️ Release Date:</strong> {game_release_date}</p>
                            <p><strong>📜 Description:</strong></p>
                            <p style="margin-left: 15px;">{game_description}</p>
                            <a href="{game_url}" style="
                                display: inline-block;
                                margin-top: 20px;
                                padding: 10px 20px;
                                background-color: #457b9d;
                                color: white;
                                text-decoration: none;
                                border-radius: 5px;
                                font-weight: bold;
                            ">
                                👉 View Game Now
                            </a>
                            <br /><br />
                            <p style="font-size: 0.9em; color: #777;">You received this email because you're subscribed to Game Art's newsletter.</p>
                        </div>
                    """
                }
            ]
        }

        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print(f"New game announcement email sent to {email.email}")
        else:
            print(f"Failed to send email: {result.status_code} - {result.json()}")


def send_mailjet_email_purchase_success(to_email, game_name, order_id, game_key):
    
    mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    data = {
        "Messages": [
            {
                "From": {
                    "Email": sender,
                    "Name": "Game Art"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": "Customer"
                    }
                ],
                "Subject": "🎮 Your Game Purchase is Complete!",
                "TextPart": (
                    f"Thank you for your purchase!\n\n"
                    f"Game: {game_name}\n"
                    f"Order ID: {order_id}\n"
                    f"Game Key: {game_key}\n\n"
                    f"Redeem your key on the appropriate platform and enjoy the game!"
                ),
                "HTMLPart": f"""
                    <div style="font-family: Arial, sans-serif; color: #333;">
                        <h2 style="color: #2d89ef;">🎉 Thank You for Your Purchase!</h2>
                        <p>We're excited to let you know that your game purchase was successful.</p>
                        <hr style="border: none; border-top: 1px solid #ccc;" />
                        <p><strong>🎮 Game:</strong> {game_name}</p>
                        <p><strong>🧾 Order ID:</strong> {order_id}</p>
                        <p><strong>🔑 Game Key:</strong> 
                            <span style="display: inline-block; padding: 10px 15px; background-color: #f3f3f3; border: 1px dashed #aaa; font-family: monospace; font-size: 1.1em;">
                                {game_key}
                            </span>
                        </p>
                        <hr style="border: none; border-top: 1px solid #ccc;" />
                        <p>You can now redeem your game key on the appropriate platform (like Steam, Epic Games, etc.).</p>
                        <p>Enjoy your game and happy gaming! 🎮</p>
                        <br />
                        <p style="font-size: 0.9em; color: #777;">If you have any questions, feel free to contact our support team.</p>
                    </div>
                """,
            }
        ]
    }

    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        print(f"Purchase confirmation email sent to {to_email}")
    else:
        print(f"Failed to send email: {result.status_code} - {result.json()}")