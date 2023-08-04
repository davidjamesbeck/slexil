FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /app
RUN mkdir assets
RUN mkdir PROJECTS
COPY *.py /app/
COPY *.txt /app/
COPY ijal.css /app/
COPY ijalUtils.js /app/
COPY jquery-3.3.1.min.js /app/
COPY assets/  /app/assets/

