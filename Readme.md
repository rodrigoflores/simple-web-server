# Python Webserver

# Description

A custom httpbin for Istio Demos

# To run natively

Install Flask and python-json-logger

```
pip install Flask==3.0.3
pip install python-json-logger==2.0.7
```

And run

```
python server.py
```

To test that it worked:
```
$ curl 0.0.0.0:5000
{"meta":{"hostname":"475a6d037cab"},"request_headers":{"Accept":"*/*","Host":"0.0.0.0:8000","User-Agent":"curl/8.7.1"}}
```

# To run as a container

```
just run
```

To test that it worked:
```
$ curl 0.0.0.0:5000
{"meta":{"hostname":"475a6d037cab"},"request_headers":{"Accept":"*/*","Host":"0.0.0.0:8000","User-Agent":"curl/8.7.1"}}
```
