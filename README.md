# AFKMonitor
A script that monitors a PC while being used or overnight. Generates a daily CSV report of computer states given time intervals.

## Usage
`python main.py <minuteInterval> <batteryThreshold> [bufferSize]`

`<minuteInterval>` is the interval in minutes at which the computer state is recorded.

The computer will shutdown when the battery percentage dips below `<batteryThreshold>`.

`[bufferSize]` (optional, default=5) is the number of computer states to store in memory before writing to the CSV file.

### Examples
`python main.py 5 20`
The computer state is recorded every 5 minutes. The computer will shutdown when the battery percentage dips below 20%.

`python main.py 15 0 10`
The computer state is recorded every 15 minutes. The computer will not shutdown. The computer states are written to the CSV in batches of 10.

`python main.py 10 -1 0`
The computer state is recorded every 10 minutes. The computer will shutdown **when unplugged**. The computer states are written to the CSV file immediately.

## Tests
`./Tests` contains tests for both performance and functionality.

To run a test, simply run `python <testName>.py`.
