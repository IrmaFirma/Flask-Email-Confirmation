from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

#secret key
s = URLSafeTimedSerializer('CODESECRET!')

#form
f = '<form style="text-align:center;"action="/"method="POST">Enter email address:<br><br><input name="email"><input type="submit"><br><br></form>'


#1 step: building a form
#1.a step: create a route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return f
    
    
    email = request.form['email']
    #2 step: generate a token
    token = s.dumps(email, salt='email-confirm')

    #send email
    msg = Message('Confirm Email', sender='irma.preldzic9@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'Please confirm email by clicking on this link. Your confirmation link is {}'.format(link)
    mail.send(msg)

    return 'A confirmation email has been sent on this {} email address.'.format(email)

#3 step: building a route for token handling
#TODO: Expired token error handling
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=600)
    except SignatureExpired:
        return 'Your link has expired. Try to submit your email again!'

    #send reply email
    msg1 = Message('Email Confirmed!', sender='irma.preldzic9@gmail.com', recipients=[email])
    msg1.body = 'Your email has been confirmed! Thank you.'
    mail.send(msg1)

    return 'Email has been confirmed. A reply message has been sent to your email address.'

if __name__ == '__main__':
    app.run(debug=True)

