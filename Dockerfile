# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY dns_proxy.py /app

# Install required Python libraries (e.g., asyncio, ssl)
RUN pip install prometheus_client

# Expose the port for both TCP and UDP DNS queries
EXPOSE 5353/tcp
EXPOSE 5353/udp

# Run the DNS proxy when the container starts
CMD ["python", "dns_proxy.py"]
