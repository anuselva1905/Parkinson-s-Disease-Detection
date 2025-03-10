from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl')
model
    
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
            spread1 = float(request.form.get("spread1", "0").strip())
            MDVP_Fo = float(request.form.get("MDVP_Fo", "0").strip())
            MDVP_Flo = float(request.form.get("MDVP_Flo", "0").strip())
            MDVP_Fhi = float(request.form.get("MDVP_Fhi", "0").strip())
            MDVP_Shimmer = float(request.form.get("MDVP_Shimmer", "0").strip())
            HNR = float(request.form.get("HNR", "0").strip())
            D2 = float(request.form.get("D2", "0").strip())

            # Print inputs for debugging
            print(f"Inputs: {spread1}, {MDVP_Fo}, {MDVP_Flo}, {MDVP_Fhi}, {MDVP_Shimmer}, {HNR}, {D2}")
             # Ensure model is loaded
            if model is None:
                return render_template('home.html', prediction_text="Model not loaded.")

            # Make prediction
            prediction = model.predict([[spread1, MDVP_Fo, MDVP_Flo, MDVP_Fhi, MDVP_Shimmer, HNR, D2]])
            output = prediction[0]

            # Define output message
            if output == 0:
                prediction_text = "The person is healthy and not at risk for Parkinson's disease."
            else:
                prediction_text = "The person has a high risk of Parkinson's disease."

            return render_template('home.html', prediction_text=prediction_text)
if __name__ == "__main__":
    app.run(debug=True)

