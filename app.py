from http.client import INTERNAL_SERVER_ERROR
from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

#secret key
s = URLSafeTimedSerializer('CODESECRET!')

#1 step: building a form
#1.a step: create a route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
    
    email = request.form['email']
    #2 step: generate a token
    token = s.dumps(email, salt='email-confirm')

    #send email
    msg = Message('Confirm Email', sender='irma.preldzic9@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'Your link is {}'.format(link)
    mail.send(msg)

    return 'The mail is {}. The token is {}'.format(email, token)

#3 step: building a route for token handling
#TODO: Expired token error handling
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=60)
    except SignatureExpired:
        return 'Link expired'
    return 'Token works!'

if __name__ == '__main__':
    app.run(debug=True)

