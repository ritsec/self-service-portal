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
- `SECRET_KEY` in `__init__.py` in the `create_app` factory
- `APP_URL` in the same factory
  * This is the URL that the user will use to access the portal, such as
    `https://portal.example.com`.
- `WEBCMD_URL` in the same factory
  * This is the URL of the WebCommander instance (see below) that the portal
    will send POST requests to.

### WebCommander Requirements
To connect the Flask application with the PowerShell scripts that it needs to
run, a "WebCommander" script/application needs to be set up.  The term
**WebCommander** refers to [VMware's WebCommander fling](https://labs.vmware.com/flings/webcommander)
which provides a way to wrap PowerShell scripts with web services.  It is not
required that you specifically use WebCommander to couple the PowerShell
scripts and Flask.  However, whatever is used to fulfill this role must adhere
to the following requirements:

- Accepts POST requests to the `/register` endpoint with the following
  parameters:
  * `fname`: The first name of the new user
  * `lname`: The last name of the new user
  * `email`: The `@rit.edu`, `@g.rit.edu`, or `@mail.rit.edu` email address of
    the new user
  * `password`: The password to give the new user
- Accepts POST requests to the `/change-password` endpoint with the following
  parameters:
  * `email`: The `@rit.edu`, `@g.rit.edu`, or `@mail.rit.edu` email address of
    the user whose password should be changed
  * `new_password`: The new password for the user
- Accepts POST data with the `application/json` MIME type
- Returns a 200 status code _only if_ the operation was successful
- Returns anything else (preferably code 400+) if the operation was not
  completed
- Uses HTTPS for all communications, since passwords are being passed around
- _Only accessible_ by the Flask instance - **nothing else** should be able to
  connect

## Compatibility Note
Some of the Javascript in this app (specifically the use of
Array.prototype.indexOf()) is not supported in Internet Explorer versions 8 and
below.  Sorry that I'm not catering to browsers that were released in 2009.  If
this is an issue, switch to a more modern browser.  In fact, just switch to a
more modern browser anyway.