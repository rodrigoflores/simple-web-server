#!/usr/bin/env python3
from flask import Flask, request, jsonify
import random
import os
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

hostname = os.getenv('HOSTNAME', 'unknown')

@app.route('/')
def request_data():
  app.logger.info('Request received')
  response = jsonify({'meta': {'hostname': hostname},
                      'request_headers': dict(request.headers)})
  return response, 200

@app.route('/random-failure/<percentage>')
def random_failure(percentage):
  random_number = random.uniform(0, 1)
  normalized_percentage = float(percentage) / 100.0
  app.logger.info(f'Random number: {random_number}, Failure threshold: {normalized_percentage}')

  status_code = 500 if random_number < normalized_percentage else 200
  response = jsonify({'meta': {'hostname': hostname,
                               'random_number': random_number,
                               'normalized_percentage': normalized_percentage,
                               'status_code': status_code,
                               'percentage': percentage},
                      'request_headers': dict(request.headers)})
  return response, 200

if __name__ == '__main__':
  app.run(debug=False)