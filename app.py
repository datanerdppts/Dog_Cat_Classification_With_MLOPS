from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.prediction_pipeline import PredictionPipeline
import base64


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)





@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')



@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    # os.system("dvc repro")
    return "Training done successfully!"




@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.predict()
    with open(clApp.filename, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    response = [
        {"prediction": result},
        {"image": encoded_string}  # returning same image back for frontend display
    ]
    return jsonify(response)



if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=8000, debug=True)
 #for AWS
