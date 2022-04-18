from flask import Flask, render_template, request
from smtplib import SMTP, SMTPResponseException, SMTPAuthenticationError
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def landing():
    return render_template('about.html')


@app.route('/contact', methods=["POST"])
def contact():
    from_email = request.form["email"]
    email_message = request.form["message"]
    name = request.form["name"]
    send_mail(from_email, email_message, name)


def send_mail(email, message, name):
    smtp_email = os.getenv("email")
    smtp_pass = os.getenv("password")

    if email == "" or name == "" or message == "":
        return render_template("email_failure.html", email=email, name=name, message=message)
    else:
        try:
            with SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=smtp_email, password=smtp_pass)
                connection.sendmail(
                    from_addr=email,
                    to_addrs="codejetsmtp@gmail.com",
                    msg=f"Subject: New Inquiry from {name} at {email}!\n\n"                       
                        f"{message}")
        except SMTPResponseException as e:
            error_message = f"Sorry we could not complete the request due to{e.smtp_error}"
            return render_template("email_failure", result=error_message)
        else:
            message = "We will be in touch with you soon, " \
                      "please allow 3 business days for us to respond"
            return render_template("email_result.html", result=message)


if __name__ == "__main__":
    app.run(debug=True)
