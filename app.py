import pandas as pd

# Load your data (modify this part to match your source)
data = {
    'datetime': ['2025-05-01 09:00:00', '2025-05-01 09:30:00', '2025-05-01 10:00:00'],
    'value': [10, 20, 30]
}
df = pd.DataFrame(data)

# Check if 'datetime' column exists
if 'datetime' in df.columns:
    # Remove any leading or trailing spaces in column names
    df.columns = df.columns.str.strip()
    
    # Convert the 'datetime' column to datetime format
    df['datetime'] = pd.to_datetime(df['datetime'])
    print(df)
else:
    print("Error: 'datetime' column not found in DataFrame.")
