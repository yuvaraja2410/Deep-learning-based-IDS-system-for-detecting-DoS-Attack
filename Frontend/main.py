from flask import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder
import sqlite3
import smtplib, ssl

app = Flask(__name__)
app.secret_key = "secret key"

# Define your email credentials
sender_email = "yuvarajait2020@mvit.edu.in"  # Replace with your email
receiver_email = "yuvarajait2020@mvit.edu.in"  # Recipient's email
password = 202004090  # Replace with your email password

# Function to send email notification
def send_email_notification():
    message = """\
    Server Under Attack Notification\n
    
    Dear User,\n\n
    
    Your server is under attack. Please take necessary actions immediately.\n\n
    
    Regards,\n
    Cyber-Shield"""
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# Load the pre-trained model and other initialization
model = load_model('model.h5')
scaler = StandardScaler()
seq_length = 10

# Define route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the uploaded CSV file
        file = request.files['file']
        file.save("Test_data.csv")
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        # Load the pre-trained model
        model = load_model('model.h5')

        # Initialize a scaler (it will be fitted on the training data)
        scaler = StandardScaler()
        seq_length = 10

        x = pd.read_csv("Test_data.csv")
        xr = x.copy()
        le_protocol_type = LabelEncoder()
        x['protocol_type'] = le_protocol_type.fit_transform(x['protocol_type'])

        le_service = LabelEncoder()
        x['service'] = le_service.fit_transform(x['service'])

        le_flag = LabelEncoder()
        x['flag'] = le_flag.fit_transform(x['flag'])
        X_scaled = scaler.fit_transform(x)

        y_pred_new = model.predict(X_scaled)
        y_pred_new = (y_pred_new > 0.5).astype(int)

        # Convert predictions to a list for easy jsonify
        predictions_list = y_pred_new.tolist()

        le_protocol_type = LabelEncoder()
        x['protocol_type'] = le_protocol_type.fit_transform(x['protocol_type'])

        le_service = LabelEncoder()
        x['service'] = le_service.fit_transform(x['service'])
        out = []
        outer = []
        v, er = 0, 0
        data = xr.values.tolist()
        for k in zip(data, predictions_list):
            r = k[0]
            if (k[1][0] == 0):
                x = "normal"
                v += 1
            else:
                x = "attacked"
                outer.append("attacked")
                er += 1
            r.append(x)
            out.append([r[1], r[2], r[-1]])
        
        # If attacked is detected, send email notification
        if outer[0] == "attacked":
            send_email_notification()
        
        # Render your template
        return render_template('prediction.html', out=out, v=v, er=er)

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/logon')
def logon():
    return render_template('signup.html')


@app.route("/signup", methods=["post"])
def signup():
    username = request.form['user']
    name = request.form['name']
    email = request.form['email']
    number = request.form["mobile"]
    password = request.form['password']
    role = "student"
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`,'role') VALUES (?, ?, ?, ?, ?,?)",
                (username, email, password, number, name, role))
    con.commit()
    con.close()
    return render_template("index.html")


@app.route("/signin", methods=["post"])
def signin():
    mail1 = request.form['user']
    password1 = request.form['password']
    con = sqlite3.connect('signup.db')
    data = 0
    data = con.execute(
        "select `user`, `password`,role,mobile from info where `user` = ? AND `password` = ?", (mail1, password1,)).fetchall()
    print(data)
    if mail1 == 'admin' and password1 == 'admin':
        session['username'] = "admin"
        return redirect("userlogin")
    elif mail1 == str(data[0][0]) and password1 == str(data[0][1]):
        print(data)
        session['username'] = data[0][0]
        session['mobile'] = data[0][3]
        return redirect("userlogin")
    else:
        return render_template("signup.html")


@app.route("/userlogin")
def userlogin():
    return render_template('checking.html')


@app.route('/logout')
def home():
    session.pop('username', None)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
