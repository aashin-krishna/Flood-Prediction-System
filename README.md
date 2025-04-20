# Flood Prediction System

A comprehensive system for predicting flood risks using sensor data, machine learning, and web interfaces.

## Features

- Real-time sensor data collection from Arduino
- Three operational modes:
  - **Web Application**: Flask-based UI for manual predictions
  - **Automated System**: Continuous sensor monitoring with Firebase logging
  - **Simple Web Interface**: Basic prediction interface
- Firebase integration for data storage
- Random Forest prediction model

## Requirements

- Python 3.7+
- Required packages: pyserial,
flask,
scikit-learn,
joblib,
firebase-admin,
numpy


## Hardware Setup

1. Arduino with flow sensors connected to COM11 (adjust in code if needed)
2. Sensors should output data in format: `1:value1,2:value2`

## Configuration

1. Rename `ServiceAccountKey.example.json` to `ServiceAccountKey.json`
2. Update Firebase database URL in code if needed
3. Place your trained model as `rf_model.joblib`

## Usage

### 1. Sensor Monitoring System
python
system = FloodPredictionSystem()
system.run()

### 2. Web Application
app = FloodPredictionApp()
app.run()  # Access at http://localhost:5000

### 3. Simple Web Interface
simple_app = SimpleFloodApp()
simple_app.run()  # Access at http://localhost:500

File Structure
flood-prediction/
├── Flood_Prediction_System.ipynb  # Main notebook
├── README.md                      # This file
├── templates/                     # Flask templates
│   ├── index.html                 # Main interface
│   ├── results.html               # Results page
│   └── results2.html              # Alternative interface
├── rf_model.joblib                # Trained model
└── ServiceAccountKey.json         # Firebase credentials

Firebase Data Structure
The system stores:

Current date/time

Sensor readings (flow1, flow2)

Rainfall values

Predicted flood levels


## Key Improvements:

1. **Modular Design**: Separated components into reusable classes
2. **Error Handling**: Added proper exception handling
3. **Configuration**: Made serial port and Firebase URL configurable
4. **Documentation**: Comprehensive docstrings and README
5. **Multiple Modes**: Can run as web app or automated sensor system
6. **Cleaner Code**: Removed duplicate functionality between scripts

To use this system:
1. Upload the notebook and README to GitHub
2. Create a `templates` folder with your HTML files
3. Add your Firebase credentials and model file
4. Run the desired components based on your needs
