curl -H "Content-Type: application/json" -X POST -d '{"t":"t"}' http://127.0.0.1:8080/kikapi_config

curl -H "Content-Type: application/json" -X POST -d '{"messages":"asdf"}' http://127.0.0.1:8080/kikapi_config
curl -H "Content-Type: application/json" -X POST -d '{"messages":[{"body":"kik welcome"}]}' http://127.0.0.1:8080/kikapi_receivemsg


curl -H "Content-Type: application/json" -X POST -d '{"t":"t"}' https://kikapi-1298.appspot.com/kikapi_config


Installing 3rd party library for webapp2 app. You need to install it to "lib" folder
pip install -t lib -r requirements.txt


local server
dev_appserver.py .



## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [NDB Datastore API][3]
- [Users API][4]

## Dependencies
- [webapp2][5]
- [jinja2][6]
- [Twitter Bootstrap][7]

[1]: https://developers.google.com/appengine
[2]: https://python.org
[3]: https://developers.google.com/appengine/docs/python/ndb/
[4]: https://developers.google.com/appengine/docs/python/users/
[5]: http://webapp-improved.appspot.com/
[6]: http://jinja.pocoo.org/docs/
[7]: http://twitter.github.com/bootstrap/


## E2E Test for this sample app

A Makefile is provided to deploy and run the e2e test.

To run:

     export GAE_PROJECT=your-project-id
     make

To manually run, install the requirements

    pip install -r e2e/requirements-dev.txt

Set the environment variable to point to your deployed app:

    export GUESTBOOK_URL="http://guestbook-test-dot-useful-temple-118922.appspot.com/"

Finally, run the test

    python e2e/test_e2e.py
