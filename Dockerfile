FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chain.py app.py ./
COPY tests/ ./tests/

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD [ "python", "app.py" ]