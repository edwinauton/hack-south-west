import json
import pandas as pd

def plotting(jsonFile):
    # Load the JSON data from the file
    with open(jsonFile) as f:
        file = json.load(f)

    # Extract high values and their corresponding time values
    high_values = []
    time_values = []
    for time_value, values in file['Time Series (5min)'].items():
        high_values.append(float(values['2. high']))
        time_values.append(pd.to_datetime(time_value))

    # Create DataFrame
    df = pd.DataFrame({'Time': time_values, 'High': high_values})

    # Plot the DataFrame
    df.plot(x='Time', y='High')
    print(df)


