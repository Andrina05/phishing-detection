import pickle
import gzip
import time
from url_processing import feature_extractor, url_fetcher
from flask import Flask,request,render_template

# Load the ML model
with gzip.open('ML_Model\phishing_model_no4_rf.pkl.gz', 'rb') as file:
    detection_model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('input_based.html')

@app.route('/predict', methods=['GET','POST'])
def predictor():
    if request.method=='POST':
        websiteurl = request.form['websiteurl']
        features = feature_extractor(websiteurl)
        model_prediction = detection_model.predict(features)
        if model_prediction[0] == 1:
            return render_template('input_based.html', prediction='Phishing')
        else:
            return render_template('input_based.html', prediction='Genuine')

@app.route('/detect')
def detect_ui():
    return render_template('real_time.html')

@app.route('/processing')
def real_time_detect():
    urls = url_fetcher()
    if urls == []:
        return render_template('real_time.html', error_line = 'Sorry, URLs could not be fetched.')
    else:
        for some_url in urls:
            time.sleep(2)
            features = feature_extractor(some_url)
            prediction = detection_model.predict(features)
            
            # yield is used to return multiple values
            if prediction[0] == 1:
                yield f'data: May be phishing: {some_url}\n\n'
            else:
                yield f'data: Safe: {some_url}\n\n'

@app.route('/phishstream')
def phishstream():
    return app.response_class(real_time_detect(), mimetype='text/event-stream')

if __name__=='__main__':
    app.run(debug=True)