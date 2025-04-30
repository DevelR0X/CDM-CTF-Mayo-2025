FROM python:3.9-slim-buster 

RUN apt update
RUN apt install -y supervisor

# Add application
WORKDIR /challenge
COPY challenge .
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN chmod -R 777 /challenge

# Setup superivsord
ADD config/supervisord.conf /etc/

# Expose the port
EXPOSE 5000

# Switch to use a non-root user from here on
USER nobody

# Start the python application
CMD /usr/bin/supervisord -c /etc/supervisord.conf