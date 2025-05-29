from mailjet_rest import Client
from blog.models import EmailSubscription
from django.conf import settings

api_key = settings.MAILJET_API_KEY
api_secret = settings.MAILJET_API_SECRET
sender = settings.SENDER

from mailjet_rest import Client

def send_mailjet_email_new_game_announcement(game_name, game_description, game_release_date, game_url):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    recipients = EmailSubscription.objects.all()

    to_list = [{"Email": sub.email, "Name": "Subscriber"} for sub in recipients]

    if not to_list:
        print("No subscribers to send to.")
        return

    subject = f"🔥 New Game Alert: {game_name} is now available!"
    text_content = (
        f"Hey gamer!\n\n"
        f"We're excited to announce a new game in our store:\n\n"
        f"🎮 Title: {game_name}\n"
        f"🗓️ Release Date: {game_release_date}\n"
        f"📝 Description:\n{game_description}\n\n"
        f"Check it out now: {game_url}\n\n"
        f"- Game Art Team"
    )

    html_content = f"""
        <div style="font-family: 'Segoe UI', sans-serif; color: #2c3e50; padding: 20px;">
            <h2 style="color: #e74c3c;">🚨 New Game Just Dropped!</h2>
            <p>Dear gamer,</p>
            <p>We're thrilled to introduce a brand new title just added to our store:</p>
            <div style="background-color: #f9f9f9; border-left: 5px solid #3498db; padding: 15px; margin: 20px 0;">
                <h3 style="color: #2980b9; margin: 0;">🎮 {game_name}</h3>
                <p><strong>🗓️ Release Date:</strong> {game_release_date}</p>
                <p><strong>📜 Description:</strong><br />{game_description}</p>
            </div>
            <a href="{game_url}" style="
                display: inline-block;
                background-color: #27ae60;
                color: white;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
            ">
                👉 Explore Game Now
            </a>
            <br /><br />
            <p style="font-size: 0.9em; color: #95a5a6;">
                You’re receiving this email because you subscribed to Game Art’s newsletter.
                If you wish to unsubscribe, please update your email preferences.
            </p>
        </div>
    """

    data = {
        "Messages": [
            {
                "From": {
                    "Email": sender,
                    "Name": "Game Art"
                },
                "To": to_list,
                "Subject": subject,
                "TextPart": text_content,
                "HTMLPart": html_content
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(f"Status: {result.status_code}, Response: {result.json()}")


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