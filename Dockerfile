FROM python:3.10.8-slim-bullseye
MAINTAINER Cory McHale <cmchale@gmail.com>
WORKDIR /hearth

# Create the hsq user.
RUN groupadd -f -g 1000 hearth
RUN useradd -o --shell /bin/bash -u 1000 -g 1000 -m hearth
#RUN echo "hearth ALL=(ALL)NOPASSWD: ALL" >> /etc/sudoers
USER hearth
WORKDIR /home/hearth

# Move application
COPY --chown=hearth:hearth requirements.txt requirements.txt
COPY --chown=hearth:hearth hearthstone/ hearthstone/
COPY --chown=hearth:hearth templates/ templates/
COPY --chown=hearth:hearth main.py .

# Install application dependancies
RUN pip3 install -r requirements.txt

# Run the API
EXPOSE 8080

CMD ["python3", "./main.py"]