from time import gmtime, strftime

def app(environ, start_response):
    data = strftime("minimal gunicorn demo: %Y-%m-%d %H:%M:%S", gmtime()).encode('UTF-8')
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])

    return iter([data])
