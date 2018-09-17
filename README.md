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

## Deployment
If you want to test deployment, there's little you have to change.  In
production this is _way_ different though.

In production, make sure to change the following things:

- `cert.pem`
- `key.pem`
- `server_name` configuration in `portal.conf` for the proxy

## Compatibility Note
Some of the Javascript in this app (specifically the use of
Array.prototype.indexOf()) is not supported in Internet Explorer versions 8 and
below.  Sorry that I'm not catering to browsers that were released in 2009.  If
this is an issue, switch to a more modern browser.  In fact, just switch to a
more modern browser anyway.