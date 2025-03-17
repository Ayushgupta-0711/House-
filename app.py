from flask import Flask, render_template, request
import mysql.connector as mc
import joblib

app = Flask(__name__)

# Database connection
conn = mc.connect(user='root', password='ayush@#11', host='localhost', database='house_p')

# Load ML model
model = joblib.load("randomforestregressor.lb")  # Ensure correct filename

# Mappings
size_dict = {
    '2 BHK': 0, '3 BHK': 1, '1 BHK': 2, '4 BHK': 3, '4 Bedroom': 4,
    '3 Bedroom': 5, '2 Bedroom': 6, '5 Bedroom': 7, '1 RK': 8,
    '5 BHK': 9, '6 BHK': 10, '6 Bedroom': 11, '11 BHK': 12,
    '7 BHK': 13, '9 BHK': 14
}

bath_dict = {
    '0.1': 0, '0.2': 1, '0.3': 2, '0.4': 3,
    '0.5': 4, '0.6': 5, '0.7': 6, '0.8': 7, '0.9': 8
}

balcony_dict = {
    '0.0': 0, '0.1': 1, '0.2': 2, '0.3': 3
}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/form')
def form():
    return render_template('userdata.html')


@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if request.method == 'POST':
        size_input = request.form['size']
        total_sqft = request.form['total_sqft']
        bath_input = request.form['bath']
        balcony_input = request.form['balcony']

        # Encoding the values
        size_encoded = size_dict.get(size_input, -1)
        bath_encoded = bath_dict.get(bath_input, -1)
        balcony_encoded = balcony_dict.get(balcony_input, -1)

        # if size_encoded == -1 or bath_encoded == -1 or balcony_encoded == -1:
            # return f"the predicted house price is :{output}"

        unseen_data = [[size_encoded, float(total_sqft), bath_encoded, balcony_encoded]]
        output = model.predict(unseen_data)[0]

        # Insert into DB
        query = """INSERT INTO pdata(size, total_sqft, bath, balcony, predicted)
                   VALUES (%s, %s, %s, %s, %s)"""
        mycursor = conn.cursor()
        details = (size_input, total_sqft, bath_input, balcony_input, int(output))
        mycursor.execute(query, details)
        conn.commit()
        mycursor.close()

        return f"The predicted house price is: {output}"

    return render_template('userdata.html')


@app.route('/history')
def history():
    conn = mc.connect(user="root", host="localhost", password="ayush@#11", database='house_p')
    mycursor = conn.cursor()

    query = "SELECT size, total_sqft, bath, balcony, predicted FROM pdata"
    mycursor.execute(query)

    data = mycursor.fetchall()

    mycursor.close()
    conn.close()

    return render_template('history.html', userdetails=data)


if __name__ == "__main__":
    app.run(debug=True)
