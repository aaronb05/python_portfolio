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
def about():
    return render_template('about.html')


@app.route('/contact', methods=["POST"])
def contact():
    from_email = request.form["email"]
    email_message = request.form["message"]
    f_name = request.form["f_name"]
    l_name = request.form["l_name"]
    if send_mail(email=from_email, message=email_message, f_name=f_name, l_name=l_name):
        return render_template("email_result.html", result=email_message)
    else:
        error_message = "Sorry, we are unable to complete you request at the moment. Please try again later!"
        return render_template("email_failure", message=error_message)


def send_mail(email, message, f_name, l_name):
    smtp_email = os.getenv("email")
    smtp_pass = os.getenv("password")
    my_email = os.getenv("personal_email")
    if email == "" or f_name == "" or l_name == "" or message == "":
        return render_template("email_failure.html", email=email, f_name=f_name, l_name=l_name, message=message)
    else:
        try:
            with SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=smtp_email, password=smtp_pass)
                connection.sendmail(
                    from_addr=smtp_email,
                    to_addrs=my_email,
                    msg=f"Subject: New message from {f_name} {l_name} at {email}!\n\n"                       
                        f"{message}")
        except SMTPResponseException as e:
            return False
        else:
            return True


if __name__ == "__main__":
    app.run(debug=True)
