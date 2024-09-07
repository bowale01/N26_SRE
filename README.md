# N26_SRE

# DNS to DNS-over-TLS Proxy

This project implements a DNS-to-DNS-over-TLS proxy, allowing conventional DNS queries over both TCP and UDP to be forwarded to a DNS server over TLS (e.g., Cloudflare).

This solution now supports multiple concurrent requests and handles both TCP and UDP DNS queries. 

## Features
- Supports **both TCP and UDP DNS queries**.
- Forwards queries to **Cloudflare's DNS-over-TLS** server.
- Uses **asyncio** to handle multiple requests concurrently.
- Fully containerized with Docker.

## Requirements
- Docker for containerized deployment
- Python 3.x if running locally

## How to Run

### Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t dns-proxy .

2. docker run -p 5353:5353 dns-proxy


Incase if you want to run it locally 

1. Install Python 3.x and dependencies.
2. Run the Python script:-
    python dns_proxy.py

The proxy will listen on port 5353 for both TCP and UDP DNS queries.

Security Concerns

Man-in-the-Middle Attacks: Since DNS-over-TLS encrypts DNS queries, a key concern would be ensuring that our proxy itself is secure. Encrypting traffic between the proxy and its clients or limiting access to internal networks only can help mitigate this.

Resource Exhaustion (DDoS):- If the proxy is exposed to the public internet, it could be a target for DDoS attacks. Rate-limiting and monitoring for suspicious activity would help protect against this.

Certificate Validation:- The proxy needs to validate the TLS certificates of the DoT server to avoid connecting to malicious servers.


Integration in a Microservices Architecture

The proxy can run as a microservice within a containerized architecture, providing DNS resolution capabilities to other services.

It can be deployed alongside services that require DNS-over-TLS to resolve domain names securely.

Services would point their DNS configuration to the proxy, ensuring that all DNS traffic is encrypted.


Improvements

1. Caching:- Implement DNS caching to reduce redundant queries and improve performance.

2. Load Balancing:- Add support for multiple DNS-over-TLS servers to distribute the load and provide redundancy.

3. Logging and Monitoring:- Implement logging eg ELK Stack for debugging and monitoring purposes eg Prometheus with Grafana for visualization.Integration with observability 

tools would provide insights into DNS query patterns and proxy health.



