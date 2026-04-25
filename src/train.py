import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'salary_data.csv'))
df.columns = df.columns.str.strip()

print(df.columns)
print(df.head())

X = df.drop('Salary', axis=1)
y = df['Salary']

X_encoded = pd.get_dummies(X)

# save these so the app knows which columns to expect
columns = X_encoded.columns.tolist()
pickle.dump(columns, open(os.path.join(BASE_DIR, 'model', 'columns.pkl'), 'wb'))

X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(f"R2 Score: {model.score(X_test, y_test):.4f}")

pickle.dump(model, open(os.path.join(BASE_DIR, 'model', 'model.pkl'), 'wb'))
print("Done - model saved")
