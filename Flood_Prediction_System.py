# %% [markdown]
"""
# Flood Prediction System

This notebook combines sensor data collection, Flask web applications, and Firebase integration for a comprehensive flood prediction system.
"""

# %% [markdown]
"""
## 1. Sensor Data Collection Module
"""
# %%
import serial
import time
import datetime

class SensorReader:
    def __init__(self, port='COM11', baud_rate=9600):
        self.serial_port = port
        self.baud_rate = baud_rate
        self.ser = None
        
    def connect(self):
        """Initialize serial connection"""
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        print("Serial connection established.")
        time.sleep(2)  # Wait for Arduino to initialize
        
    def read_data(self):
        """Read and parse sensor data"""
        if not self.ser:
            self.connect()
            
        data = self.ser.readline().decode().strip()
        sensor_data = {}
        
        for sensor_value in data.split(','):
            try:
                sensor_id, value = sensor_value.split(':')
                sensor_data[int(sensor_id)] = float(value)
            except:
                continue
                
        return sensor_data
    
    def close(self):
        """Close serial connection"""
        if self.ser:
            self.ser.close()
            print("Serial connection closed.")

# Example usage
sensor_reader = SensorReader()
try:
    sensor_data = sensor_reader.read_data()
    print("Sensor Data:", sensor_data)
finally:
    sensor_reader.close()

# %% [markdown]
"""
## 2. Flask Web Application Modules
"""
# %%
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

class FloodPredictionApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.model = joblib.load('rf_model.joblib')
        self.setup_routes()
        
    def scale_input(self, input_data):
        """Implement your scaling logic here"""
        return np.array([input_data])
    
    def setup_routes(self):
        """Configure Flask routes"""
        
        @self.app.route('/')
        def home():
            return render_template('index.html')
            
        @self.app.route('/predict', methods=['POST'])
        def predict():
            try:
                input_data = [
                    float(request.form['feature1']),
                    float(request.form['feature2']),
                    float(request.form['feature3'])
                ]
                scaled_input = self.scale_input(input_data)
                prediction = self.model.predict(scaled_input)[0][0]
                return jsonify({'prediction': prediction})
            except Exception as e:
                return jsonify({'error': str(e)})
    
    def run(self):
        """Run the Flask app"""
        self.app.run(debug=True)

# Uncomment to run the app
# app = FloodPredictionApp()
# app.run()

# %% [markdown]
"""
## 3. Firebase Integration Module
"""
# %%
import firebase_admin
from firebase_admin import credentials, db

class FirebaseManager:
    def __init__(self):
        self.cred = credentials.Certificate("./ServiceAccountKey.json")
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': "https://floodprediction-108b6-default-rtdb.firebaseio.com/"
        })
        self.db_ref = db.reference("")
        
    def update_data(self, sensor_data, predictions):
        """Update Firebase with sensor data and predictions"""
        current_datetime = datetime.datetime.now()
        update_data = {
            'date': current_datetime.strftime('%d'),
            'month': current_datetime.strftime('%m'),
            'year': current_datetime.strftime('%Y'),
            'flow1': sensor_data.get(1, 0.0),
            'flow2': sensor_data.get(2, 0.0),
            'rainflow1': 1.2,  # Example values
            'rainflow2': 1.3,
            'level1': predictions[0],
            'level2': predictions[1]
        }
        self.db_ref.update(update_data)
        print("Data updated to Firebase")

# Example usage
# firebase = FirebaseManager()
# firebase.update_data({1: 10.5, 2: 8.3}, [3.2, 2.8])

# %% [markdown]
"""
## 4. Main Prediction System
"""
# %%
class FloodPredictionSystem:
    def __init__(self):
        self.sensor_reader = SensorReader()
        self.firebase = FirebaseManager()
        self.model = joblib.load('rf_model.joblib')
        
    def run(self):
        try:
            self.sensor_reader.connect()
            
            while True:
                # Read sensor data
                sensor_data = self.sensor_reader.read_data()
                print("Sensor Data:", sensor_data)
                
                # Prepare prediction inputs
                current_datetime = datetime.datetime.now()
                input_data1 = [
                    current_datetime.strftime('%d'),
                    current_datetime.strftime('%m'),
                    current_datetime.strftime('%Y'),
                    sensor_data.get(1, 0.0),
                    1.2  # Example rainfall value
                ]
                
                input_data2 = [
                    current_datetime.strftime('%d'),
                    current_datetime.strftime('%m'),
                    current_datetime.strftime('%Y'),
                    sensor_data.get(2, 0.0),
                    1.3  # Example rainfall value
                ]
                
                # Make predictions
                level1 = self.model.predict([input_data1])[0]
                level2 = self.model.predict([input_data2])[0]
                print(f"Predictions: Level1={level1}, Level2={level2}")
                
                # Update Firebase
                self.firebase.update_data(sensor_data, [level1, level2])
                
                time.sleep(5)  # Wait before next reading
                
        except KeyboardInterrupt:
            print("Stopping system...")
        finally:
            self.sensor_reader.close()

# Uncomment to run the complete system
# system = FloodPredictionSystem()
# system.run()

# %% [markdown]
"""
## 5. Alternative Flask App (Simple Version)
"""
# %%
class SimpleFloodApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.model = joblib.load('rf_model.joblib')
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template('results2.html')
            
        @self.app.route('/predict', methods=['POST'])
        def predict():
            date = request.form['date']
            month = request.form['month']
            year = request.form['year']
            flow = float(request.form['flow'])
            rainfall = float(request.form['rainfall'])
            
            input_data = [[date, month, year, flow, rainfall]]
            prediction = self.model.predict(input_data)
            
            return render_template('results.html', prediction=prediction)
    
    def run(self):
        self.app.run(debug=True)

# Uncomment to run the simple app
# simple_app = SimpleFloodApp()
# simple_app.run()