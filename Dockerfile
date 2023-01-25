FROM python:3.9-bullseye

ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Install the Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy the application files
COPY --chown=appuser . /app

# Run the application
CMD ["python", "app/app.py"]
