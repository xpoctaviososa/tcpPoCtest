from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
  
# Start Flask Process
if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0', port=8080)#, ssl_context=context)#threaded=True)
#
# Rename App to Application for WSGI
application = app
