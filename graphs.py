import pandas as pd
import json
import matplotlib.pyplot as plt

def plotting(jsonFile):
    # Load the JSON data from the file
    with open(jsonFile) as f:
        file = json.load(f)


    ## adapt to json input:
    ## for time, values in jsonFile['Time Series (5min)].items():
    ##  ...


    # Extract high values and their corresponding time values
    high_values = []
    time_values = []
    for time_value, values in file['Time Series (5min)'].items():
        high_values.append(float(values['2. high']))
        time_values.append(pd.to_datetime(time_value))

    # Create DataFrame
    df = pd.DataFrame({'Time': time_values, 'High': high_values})

    # Plot the DataFrame using matplotlib
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    plt.plot(df['Time'], df['High'], marker='o', linestyle='-')  # Plot the data
    plt.title('High Values Over Time')  # Set the title of the plot
    plt.xlabel('Time')  # Set the x-axis label
    plt.ylabel('High')  # Set the y-axis label
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability (optional)
    plt.tight_layout()  # Adjust the layout to make room for the rotated x-axis labels (optional)
    plt.show()  # Display the plot

    return df

plotting("resources/2023-01_hourly_AAPL.json")
