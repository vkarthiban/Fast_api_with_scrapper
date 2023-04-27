# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port that the FAST API application will run on
EXPOSE 8000
CMD [ "python", "manage_db.py"]
# Start the FAST API application when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


RUN apt-get update && \
    apt-get -y install cron

# Copy the Python script to the container
COPY script.py /usr/src/app/

# Add the cron job to the crontab file
RUN echo "0 8 * * * python /app/scrapper.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/my-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron

# Apply the cron job
RUN crontab /etc/cron.d/my-cron

# Run the command on container startup
CMD ["cron", "-f"]