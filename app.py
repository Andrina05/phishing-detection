import pickle
import gzip
from url_processing import feature_extractor
from flask import Flask,request,render_template
from flask_cors import cross_origin

"""
For looping through a list of URLs
def detector(urls):
    for some_url in urls:
        features = feature_extractor(some_url)
        prediction = detection_model.predict(features)
        if prediction[0] == 1:
            print(f'This URL may be a phishing URL: {some_url}')
        else:
            print(f'This URL is safe: {some_url}')
"""
# Load the ML model
with gzip.open('ML_Model\phishing_model_no4_rf.pkl.gz', 'rb') as file:
    detection_model = pickle.load(file)

app = Flask(__name__)

@app.route('/', endpoint='home')
def homepage():
    return render_template('home.html')

@app.route('/predict', methods=['GET','POST'], endpoint='predict')
def predictor():
    if request.method=='POST':
        websiteurl = request.form['websiteurl']
        features = feature_extractor(websiteurl)
        model_prediction = detection_model.predict(features)
        if model_prediction[0] == 1:
            return render_template('home.html', prediction='Phishing')
        else:
            return render_template('home.html', prediction='Genuine')

if __name__=='__main__':
    app.run(debug=True)