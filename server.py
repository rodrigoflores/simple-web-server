#!/usr/bin/env python3
from flask import Flask, request, jsonify, g
import random
import os
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, make_wsgi_app, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

app = Flask(__name__)

in_request_counter = Counter('http_in_requests', 'Requests received', ["path", "method", "user_agent"])
in_response_counter = Counter('http_in_responses', 'Responses sent', ["path", "method", "user_agent", "status_code"])
in_response_latency = Histogram('http_in_response_latency', 'Response latency', ["path", "method", "user_agent", "status_code"])

hostname = os.getenv('HOSTNAME', 'unknown')

@app.before_request
def count_requests():
  method = request.method
  path = request.path
  user_agent = request.headers.get('User-Agent')
  in_request_counter.labels(path=path, user_agent=user_agent, method=method).inc()
  g.start_time = time.time()

@app.after_request
def count_responses(response):
  method = request.method
  path = request.path
  user_agent = request.headers.get('User-Agent')
  status_code = response.status_code
  in_response_counter.labels(path=path, user_agent=user_agent, method=method, status_code=status_code).inc()

  duration = time.time() - g.start_time
  app.logger.info(f'Request duration: {duration}')
  in_response_latency \
    .labels(path=path, user_agent=user_agent, method=method, status_code=status_code) \
    .observe(duration)
  return response

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
  return response, status_code

if __name__ == '__main__':
  app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
  })
  app.run(debug=False, port=8080, host='0.0.0.0')