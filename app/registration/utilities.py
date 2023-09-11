from ..email import send_email

def send_password_reset_email(user):
    token = user.get_reset_credential_token()
    send_email('[Ripoti Taka Program] Reset Your Password', 
            sender = flask.current_app.config['COMMUNICATIONS_EMAIL'],
            recipients = [user.email],
            text_body = flask.render_template('email/reset_password.txt', 
                user = user, token = token), 
            html_body = flask.render_template('email/reset_password.html', 
                user = user, token = token))
