from mailjet_rest import Client
from django.conf import settings

api_key = settings.MAILJET_API_KEY
api_secret = settings.MAILJET_API_SECRET

def send_mailjet_email_purchase_success(to_email, game_name, order_id, game_key):
    mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    data = {
        "Messages": [
            {
                "From": {
                    "Email": "minhnguyen47431@gmail.com",
                    "Name": "Your Game Store"
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