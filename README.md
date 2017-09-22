# Bus Prediction Accuracy Reports Parser

This is a little Python script to parse out the prediction accuracy reports. To use it:

1. Put the reports into the `/data/` directory.
2. Change the `start_date` and `end_date` values in `parser.py`.
3. Run `parser.py`. This generates a file called `output.csv` which can be manipulated in your program of choice.

Currently it uses two different thresholds, four routes plus "all routes", and it splits dates into "Weekday" or "Weekend." In the future we could make these all configurable.
