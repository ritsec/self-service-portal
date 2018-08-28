# self-service-portal
The self-service portal for RITSEC accounts

## Testing
First, install the python dependencies with `pip install -r requirements.txt`.
It is recommended you perform this step in a virtual environment.

To run a development copy (with debugging and other nice features), set the
following environment variables:
```
FLASK_APP=portal
FLASK_ENV=development
```

Finally, run the server with `flask run`.  The test server will run locally on
port 5000, and the PIN to the debugger will be printed in the output once the
server starts.