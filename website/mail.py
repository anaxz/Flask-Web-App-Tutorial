from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

# configuration -> you would put this in __init__ instead
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465' # gmail's port
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')  #OR MANUAL 'INSERT UR PASS HERE'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        msg = Message("Hey", sender='noreply@demo.com',
                        recipients=['youremail@gmail.com'])
        msg.body = "Hey how are you? Iseverything okay?"
        mail.send(msg)
        return "Send email"
    return render_template('index.html')

# if __name__=='__main__':
#     app.run(debug=True)

## note: this was made for gmail but now outdated, would need to use another email provider
#REF: https://www.youtube.com/watch?v=L7Cslucyyyo