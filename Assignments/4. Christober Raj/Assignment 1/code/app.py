from flask import Flask, render_template, request
import requests
from email_validator import validate_email, EmailNotValidError
import python_avatars as pa
from dateutil import parser, relativedelta
from datetime import date

SITE_NAME = 'Christober Raj'
app = Flask(__name__)
app.jinja_env.globals['SITE_NAME'] = SITE_NAME


# Views
@app.route('/', methods=['GET'])
def index():
    return render_template('register.html')


@app.route('/success', methods=['POST'])
def success():
    return render_template('success.html', form_data=request.form)


@app.route('/validator', methods=['GET', 'POST'])
def email_validator():
    if request.method == 'GET':
        return render_template('validator.html', email='')
    elif request.method == 'POST':
        valid = False
        try:
            validate_email(request.form['email'],
                           check_deliverability=True)
            valid = True
        except EmailNotValidError:
            pass

        return render_template('validator.html', email=request.form['email'],
                               valid=valid)


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'GET':
        return render_template('check.html', site='')
    elif request.method == 'POST':
        site = request.form['site']
        try:
            response = requests.get('https://' + site)
            status = response.status_code == 200
        except:
            status = False
        return render_template('check.html', site=site, status=status)


@app.route('/avatar', methods=['GET'])
def avatar():
    avatar_img = pa.Avatar.random()
    return render_template('avatar.html', avatar=avatar_img.render())


@app.route('/age', methods=['GET', 'POST'])
def age_calculator():
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    if request.method == 'GET':
        return render_template('age.html', dob='', today=today_str)
    elif request.method == 'POST':
        dob = request.form['dob']
        age = relativedelta.relativedelta(today,
                                          parser.parse(dob)).years
        if age < 0:
            age = 0
        return render_template('age.html', dob=dob, today=today_str, age=age)


if __name__ == '__main__':
    app.run(
        debug=True
    )
