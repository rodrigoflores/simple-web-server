from flask import Flask, request, jsonify
import logging
import os
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

hostname = os.getenv('hostname', 'unknown')

@app.route('/')
def request_data():
  app.logger.info('Request received')
  response = jsonify({'meta': {'hostname': hostname},
                      'request_headers': dict(request.headers)})
  return response, 200

if __name__ == '__main__':
  app.run(debug=True)