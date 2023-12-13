# pull python:latest image
FROM python:latest

# set working directory
WORKDIR /app

# copy all files from current directory to /app in container
COPY the_app.py /app
COPY requirements.txt /app


# set environment variables

ENV SUBSCRIPTION_KEY="--"
ENV REGION="--"

# Install libssl1.1 from a specific repository
RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list.d/bullseye.list && \
    apt-get update && \
    apt-get install -y libssl1.1 libasound2



RUN pip install -r requirements.txt

EXPOSE 8501


# run app.py at container launch
CMD ["streamlit", "run", "the_app.py"]
