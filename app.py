import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import joblib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flask_session'

# In-memory storage instead of MySQL database
# This will reset every time the server restarts
users_db = {'admin': {'password': 'admin123', 'role': 'admin'}}
predictions_db = []
prediction_id_counter = 1

# Load Model
try:
    model = joblib.load('crop_model.pkl')
    crop_dict = joblib.load('crop_dict.pkl')
except FileNotFoundError:
    print("Model files not found. Please run model.py to generate them.")
    model = None
    crop_dict = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            flash('Username might already exist.', 'danger')
        else:
            role = 'admin' if len(users_db) == 0 else 'user'
            users_db[username] = {'password': password, 'role': role}
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
    return render_template('login.html', is_register=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_db.get(username)
        if user and user['password'] == password:
            session['user_id'] = username
            session['username'] = username
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard') if user['role'] == 'admin' else url_for('predict'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html', is_register=False)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global prediction_id_counter
    if 'user_id' not in session:
        flash('Please log in to make a prediction.', 'warning')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        if not model or not crop_dict:
            flash('Machine learning model is not available.', 'danger')
            return redirect(url_for('predict'))
            
        crop_name = request.form['crop_name']
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        fertilizer = float(request.form['fertilizer'])
        area = float(request.form['area'])
        
        crop_encoded = crop_dict.get(crop_name, 0)
        
        # Make prediction
        prediction = model.predict([[crop_encoded, rainfall, temperature, humidity, fertilizer, area]])[0]
        predicted_yield = round(prediction, 2)
        
        # Save to in-memory database
        predictions_db.append({
            'id': prediction_id_counter,
            'user_id': session['username'],
            'username': session['username'],
            'crop_name': crop_name,
            'rainfall': rainfall,
            'temperature': temperature,
            'humidity': humidity,
            'fertilizer': fertilizer,
            'area': area,
            'predicted_yield': predicted_yield,
            'prediction_date': datetime.now()
        })
        prediction_id_counter += 1
            
        return render_template('result.html', yield_val=predicted_yield, crop=crop_name, area=area)
        
    return render_template('predict.html', crops=crop_dict.keys() if crop_dict else [])

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    if session['role'] == 'admin':
        records = sorted(predictions_db, key=lambda x: x['prediction_date'], reverse=True)
    else:
        records = sorted([p for p in predictions_db if p['user_id'] == session['username']], key=lambda x: x['prediction_date'], reverse=True)
        
    return render_template('dashboard.html', records=records)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    if 'user_id' not in session or session['role'] != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    global predictions_db
    predictions_db = [p for p in predictions_db if p['id'] != id]
    return jsonify({'success': True})

@app.route('/chart_data')
def chart_data():
    if 'user_id' not in session:
        return jsonify([])
        
    if session['role'] == 'admin':
        relevant_records = predictions_db
    else:
        relevant_records = [p for p in predictions_db if p['user_id'] == session['username']]
        
    # Group by crop_name and average yield
    crop_yields = {}
    for p in relevant_records:
        crop_yields.setdefault(p['crop_name'], []).append(p['predicted_yield'])
        
    data = [{'crop_name': crop, 'avg_yield': sum(yields)/len(yields)} for crop, yields in crop_yields.items()]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
