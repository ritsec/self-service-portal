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
Before deploying, make sure to review `portal.env`.  Uncomment all commented
configurations and follow the directions in the file for setting the proper
values.  Then, simply run `sudo docker-compose up` in the root directory.
You're good to go!  The portal is listening on IPv4 port 443 on the docker
host.

## Compatibility Note
Some of the Javascript in this app (specifically the use of
Array.prototype.indexOf()) is not supported in Internet Explorer versions 8 and
below.  Sorry that I'm not catering to browsers that were released in 2009.  If
this is an issue, switch to a more modern browser.  In fact, just switch to a
more modern browser anyway.

## Email Link Note
The "magic links" that are generated and emailed to users are not checked for
duplicates.  There is sufficient entropy space that there should _never_ be a
collision.  If a collision happens, either there's a serious bug in someone's
code somewhere, or you should go buy **all the lottery tickets**.

Also, these links expire after _four hours_, or once someone submits the form
associated with the link - note that only one submission will work!  If you
submit the form and get an error, you have to go generate another email code.
I may change this if it gets to be a big deal.