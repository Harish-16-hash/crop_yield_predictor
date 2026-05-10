import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

def create_dummy_model():
    print("Generating dummy dataset for Crop Yield Prediction...")
    # Generate dummy data
    np.random.seed(42)
    n_samples = 1000
    
    crops = ['Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton']
    data = {
        'crop_encoded': np.random.randint(0, len(crops), n_samples),
        'rainfall': np.random.uniform(500, 2500, n_samples),
        'temperature': np.random.uniform(15, 40, n_samples),
        'humidity': np.random.uniform(30, 90, n_samples),
        'fertilizer': np.random.uniform(50, 300, n_samples),
        'area': np.random.uniform(1, 50, n_samples)
    }
    
    # Calculate yield with some formula + noise
    yield_base = (data['rainfall'] * 0.01) + (data['temperature'] * 0.1) + \
                 (data['humidity'] * 0.05) + (data['fertilizer'] * 0.02)
    
    # Add crop specific multipliers
    crop_mults = [1.2, 1.5, 1.0, 2.5, 0.8]
    yield_mult = np.array([crop_mults[c] for c in data['crop_encoded']])
    
    # Yield in tons per hectare (approximate realistic ranges)
    data['yield'] = (yield_base * yield_mult / data['area']) + np.random.normal(0, 0.5, n_samples)
    data['yield'] = np.maximum(data['yield'], 0.5) # Ensure positive yield
    
    df = pd.DataFrame(data)
    
    # Features and Target
    X = df[['crop_encoded', 'rainfall', 'temperature', 'humidity', 'fertilizer', 'area']]
    y = df['yield']
    
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save the model
    joblib.dump(model, 'crop_model.pkl')
    print("Model saved to 'crop_model.pkl'")
    
    # Save the crop mapping dictionary
    crop_dict = {crop: idx for idx, crop in enumerate(crops)}
    joblib.dump(crop_dict, 'crop_dict.pkl')
    print("Crop mapping saved to 'crop_dict.pkl'")

if __name__ == '__main__':
    create_dummy_model()
