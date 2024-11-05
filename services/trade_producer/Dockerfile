FROM python:3.10.3-slim-buster

# Add /app to the Python path
ENV PYTHONPATH=/app

# Stream output to console
ENV PYTHONUNBUFFERED=1

# cinstall python poetry
RUN pip install poetry==1.8.2

# set the working directory in the container
WORKDIR /app

# copy the source code to the working directory
COPY . /app

# install dependencies
RUN poetry install

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]

