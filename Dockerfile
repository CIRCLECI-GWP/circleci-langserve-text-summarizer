FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chain.py app.py ./
COPY tests/ ./tests/

# Make port 80 available to the world outside this container
EXPOSE 80

# Create a non-root user and switch to it
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Run app.py when the container launches
CMD [ "python", "app.py" ]