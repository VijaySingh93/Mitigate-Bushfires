import os
from flask import Flask, render_template, flash, redirect, url_for, request
from twilio.rest import Client 
from forms import report
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Austrailian Bushfires'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(basedir, 'uploads')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


@app.route("/")
def home():
    return render_template('main.html')

@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/map")
def map():
    return render_template('australia_bushfire1.html')

@app.route("/map1")
def map1():
    return render_template('australia_bushfire.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    form = report()
    file_url = None
    res = None
    if request.method == 'GET':
        # placeholder to check if any region was having fire on the current date previous years.
        return render_template('forecast.html', form=form, file_url=file_url, res=res)
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = photos.save(form.image.data)
            file_url = photos.url(filename)
            # placeholder to identify if the uploaded image is of a fire
            name = request.form.get('name')
            region = request.form.get('region')
            phone = request.form.get('phone')
            # Your Account Sid and Auth Token from twilio.com / console 
            account_sid = '<Your Account id>'
            auth_token = '<Your token>'
            
            client = Client(account_sid, auth_token) 
            try:
                message1 = client.messages.create( 
                                            from_='+16084715116', 
                                            body ='{} has reported an incident in the region of {}. It has 78% probability of a bushfire'.format(name,region), 
                                            to = '+61408695029'
                                        )
                message2 = client.messages.create( 
                                            from_='+16084715116', 
                                            body ='Fire History Alert! People in MALLEE, WIMMERA areas. Please be vigilant as last year you had bush fires during these days.', 
                                            to = '+61408695029'
                                        )
                print(message1.sid)                         
                print(message2.sid)
                res = 'Thank You for the details! The concerned authorities have been notified'
            except Exception as e:
                res = 'SMS Alert failed with error:{}'.format(e) 
            
    return render_template('forecast.html', form=form, file_url=file_url, res=res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
