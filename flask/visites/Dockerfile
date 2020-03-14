FROM fedora:27
#WORKDIR /app
#ADD . /app
#RUN pip install --trusted-host pypi.python.org  requirements.txt
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN dnf -y install python3 python3-pip
RUN pip3 install Flask Redis
EXPOSE 80
ENV NAME World
CMD ["python3", "app.py"]
