from flask import Flask
from frontend.views import frontend


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app = Flask(__name__)
app.register_blueprint(frontend)
