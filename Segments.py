from __future__ import print_function
import sys
import urllib3, requests, json, os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FloatField, IntegerField,SelectField
from wtforms.validators import Required, Length, NumberRange



app = Flask(__name__)
#app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = 'my top secret secret'
bootstrap = Bootstrap(app)

class SurvivorForm(FlaskForm):
    MyField = SelectField(
        'Label 2',
        choices=[("style and fashion","Style and Fashion"),
("technology and computing","Technology and Computing"),
("art and entertainment","Art and Entertainment"),
("home and garden","Home and Garden"),
("business and industrial","Business and Industrial"),
("food and drink", "Food and Drink"),
("sports","Sports")]
    )

    MyField2 = SelectField(
        'Label 3',
        choices=[("jewelry","Jewelry"),
("software","Software"),
("internet technology","Internet Technology"),
("appliances","Appliances"),
("None","None"),
("consumer electronics","Consumer Electronics"),
("business operations","Business Operations"),
("clothing","Clothing"),
("hardware","Hardware"),
("pest control","Pest Control"),
("football","Football"),
("manufacturing","Manufacturing")]
    )

    MyField3 = SelectField(
        'Company Size',
        choices=[("small","small"),
("medium","medium"),
("large","large")]
    )

    MyField4 = SelectField(
        'Type',
        choices=[("Privately Held","Privately Held"),
("Public Company","Public Company"),
("Private Company","Private Company"),
("Private Ltd","Private Ltd"),
("Self Owned","Self Owned"),
("Non Profit","Non Profit"),
("Unknown","Unknown")]
    )

    MyField5 = SelectField(
        'Country',
        choices=[("United States","United States"),
("United Kingdom","United Kingdom"),
("India","India"),
("China","China"),
("Netherlands","Netherlands"),
("Italy","Italy"),
("Korea","Korea"),
("Brazil","Brazil"),
("Sweden","Sweden"),
("Australia","Australia"),
("Canada","Canada"),
("France","France"),
("Germany","Germany"),
("Finland","Finland"),
("Lebanon","Lebanon"),
("Mexico","Mexico"),
("Switzerland","Switzerland"),
("Czech Republic","Czech Republic"),
("Poland","Poland"),
("Hungary","Hungary"),
("Portugal","Portugal"),
("Spain","Spain"),
("Pakistan","Pakistan"),
("Bulgaria","Bulgaria"),
("Japan","Japan"),
("Belgium","Belgium"),
("Estonia","Estonia"),
("Austria","Austria"),
("Romania","Romania"),
("Serbia and Montenegro","Serbia and Montenegro")]
    )
                                                 
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    
    #result = None
    #response_scoring = None
    form = SurvivorForm()
    #if request.method == 'POST':
    if form.validate_on_submit():

        Label2 = form.MyField.data
        form.MyField.data = ''
        Label3 = form.MyField2.data
        form.MyField2.data = ''
        CoSize = form.MyField3.data
        form.MyField3.data = ''
        Type = form.MyField4.data
        form.MyField4.data = ''
        Country = form.MyField5.data
        form.MyField5.data = ''


        
        service_path = 'https://ibm-watson-ml.mybluemix.net'
        username = '10968592-11ba-4515-acab-6ebbb1680289'
        password = '1041dd02-7085-4c67-a3a7-dea6c8a0c32d'

        headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
        url = '{}/v2/identity/token'.format(service_path)
        response = requests.get(url, headers=headers)
        mltoken = json.loads(response.text).get('token')
        header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
        scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/2596"
        payload_scoring = {"record":[Type, Country, CoSize, Label2, Label3]}

        print(payload_scoring, file=sys.stderr)

        response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
        result = response_scoring.text
        
        data = request.form

        return render_template('score.html', form=form, result=result, data=data, response_scoring=response_scoring)
    
    
    return render_template('index.html', form=form)
    
    
@app.route('/scoretest', methods=['GET', 'POST'])
def scoretest():



    
    service_path = 'https://ibm-watson-ml.mybluemix.net'
    username = '10968592-11ba-4515-acab-6ebbb1680289'
    password = '1041dd02-7085-4c67-a3a7-dea6c8a0c32d'

    headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
    url = '{}/v2/identity/token'.format(service_path)
    response = requests.get(url, headers=headers)
    mltoken = json.loads(response.text).get('token')
    header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
    scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/2596"
    #payload_scoring = {"record":["Privately Held","United States", "small", "style and fashion", 'jewelry']}
    payload_scoring ={'record': [u'Privately Held', u'United States', u'small', u'style and fashion', u'None']}

    response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
    
    result = response_scoring.text
    return render_template('scoretest.html', result=result, response_scoring=response_scoring)
    


#if __name__ == '__main__':
#	app.run(debug=True)
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

