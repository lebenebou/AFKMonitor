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

We will also add machine learning models...