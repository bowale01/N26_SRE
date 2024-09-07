# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the proxy script to the container
COPY dns_proxy.py /app

# Install dependencies (if necessary)
# RUN pip install ...

# Expose the port on which the DNS proxy listens
EXPOSE 5353

# Command to run the DNS proxy
CMD ["python", "dns_proxy.py"]
