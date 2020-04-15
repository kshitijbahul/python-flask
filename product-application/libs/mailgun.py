import os
from requests import Response,post
from typing import List

class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_EMAIL ="mailgun@{MAILGUN_DOMAIN}"
    FROM_TITLE = "Product Service"
    
    @classmethod
    def send_email(cls,email: List[str], subject: str,text: str,html: str) -> Response:
            print(cls.MAILGUN_DOMAIN)
            #talk to mailgun
            #respond
            #upto not including the last info, name of the resource for user confirm
            response = post(
                "https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
                auth = ("api","{cls.MAILGUN_API_KEY}"),
                data={"from": "{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                    "to":email,
                    "subject": subject,
                    "text": text,
                    "html": html
                },
            )
            print(response)
            return response