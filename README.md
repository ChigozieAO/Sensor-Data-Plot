# Sensor-Data-Plot
Python tool for logging and visualising voltage, current, and temperature sensor data from CSV files.

Reads voltage, current, and temperature readings from a CSV file and plots them as a time-series dashboard. Includes a fake data generator for testing.

## Usage
 
**Generate test data:**
- python generate_data.py

 
**Plot the data:**
- python plot_sensor_data.py                                # display interactively
- python plot_sensor_data.py --save                         # save as sensor_plot.png
- python plot_sensor_data.py --file my_data.csv             # use a different file
- python plot_sensor_data.py --save --output (name).png     # save with a custom output name

 
## Dependencies
 
- `matplotlib` — everything else is standard library
