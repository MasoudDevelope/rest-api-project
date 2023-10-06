import requests
import os
from dotenv import load_dotenv
import jinja2


load_dotenv()

domain =os.getenv("MAILGUN_DOMAIN")
api_key=os.getenv("MAILGUN_API_KEY")
template_loader = jinja2.FileSystemLoader("templates")
template_env= jinja2.Environment(loader=template_loader)

def render_template (template_filename,**context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to,subject,body,html):
    return  (requests.post(
		f"https://api.mailgun.net/v3/{domain}/messages",
		auth=("api", api_key),
		data={"from": f"HR <mailgun@{domain}>",
			"to": [to],
			"subject": subject,
			"text":body ,
            "html":html
            }))

def func_send_simple_message(email,username):
    return send_simple_message(
        email,
        "sign up successful",
        f"Hi {username}, You have successfully signed up to the stores REST API",
        render_template("email/action.html",username=username)
    )