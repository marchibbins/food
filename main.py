from flask import Flask
from frontend.views import frontend, frontend_errors


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app = Flask(__name__)
app.register_blueprint(frontend)
frontend_errors(app)
