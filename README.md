# AFKMonitor
A script that monitors a PC overnight. Generates a daily CSV report of computer states at chosen intervals.

## Usage
`python monitor.py <minuteInterval> <batteryThreshold> [bufferSize]`

`<minuteInterval>` is the interval in minutes at which the computer state is recorded.

The computer will shutdown when the battery percentage dips below `<batteryThreshold>`.

`[bufferSize]` (optional, default=5) is the number of computer states to store in memory before writing to the CSV file.

### Examples
`python monitor.py 5 20`
The computer state is recorded every 5 minutes. The computer will shutdown when the battery percentage dips below 20%.

`python monitor.py 15 0 10`
The computer state is recorded every 15 minutes. The computer will not shutdown. The computer states are written to the CSV in batches of 10.

`python monitor.py 10 -1 0`
The computer state is recorded every 10 minutes. The computer will shutdown **when unplugged**. The computer states are written to the CSV file immediately.

## Tests
`./Tests` contains tests for both performance and functionality.

To run a test, simply run `python <testName>.py`.

## Machine Learning
We will also add Machine Learning.

## Data Science
We will also add Visualisation.

### Visualizations
#### 1. Battery Percentage Over Time
   - Line plot displaying the variation in battery percentage throughout the selected date.

#### 2. Memory Usage of Processes
   - Bar chart showing the memory usage of the top processes on the selected date.

#### 3. Network Activity
   - Line plot depicting bytes sent and received over time on the selected date.

#### 4. Running Processes
   - Line plot illustrating the number of running processes over time.

### Analysis
The script provides various analyses on the selected date:
- Battery Analysis:
  - Average, minimum, and maximum battery percentages.

- Memory Usage Analysis:
  - Total memory usage and top processes by memory usage.

- Network Activity Analysis:
  - Total bytes sent and received.

- Running Processes Analysis:
  - Average number of running processes.

- Charging and Connected Analysis:
  - Percentage of time the device was charging.
  - Percentage of time the device was connected.

- Process Analysis:
  - Most frequently running processes.

- Hungry Process Analysis:
  - Process with the highest memory usage.

- Memory Usage Trends:
  - Trends in memory usage resampled on an hourly basis.

### Error Handling
- If the user provides an invalid date format or if no data is available for the selected date, the script displays an error message and exits.
