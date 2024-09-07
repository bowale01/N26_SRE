import socket
import ssl
import asyncio

# Constants for Cloudflare DNS-over-TLS server
DOT_SERVER = "1.1.1.1"
DOT_PORT = 853

# Proxy's listening ports for TCP and UDP
PROXY_TCP_PORT = 5353
PROXY_UDP_PORT = 5353

BUFFER_SIZE = 1024  # Adjust buffer size if necessary

async def forward_to_dot(query_data):
    """Forward the DNS query to the DNS-over-TLS server."""
    context = ssl.create_default_context()

    # Establish a TCP connection to the DoT server with TLS wrapping
    reader, writer = await asyncio.open_connection(DOT_SERVER, DOT_PORT, ssl=context)
    
    # Send the DNS query to Cloudflare DoT
    writer.write(query_data)
    await writer.drain()

    # Receive the response from Cloudflare
    response_data = await reader.read(BUFFER_SIZE)
    
    writer.close()
    await writer.wait_closed()
    
    return response_data

async def handle_tcp_client(reader, writer):
    """Handle a single TCP client."""
    query_data = await reader.read(BUFFER_SIZE)  # Receive DNS query

    # Forward the query to the DoT server and get the response
    response_data = await forward_to_dot(query_data)

    # Send the response back to the client
    writer.write(response_data)
    await writer.drain()
    
    writer.close()

async def handle_udp_client(data, addr, udp_server):
    """Handle a single UDP client."""
    # Forward the query to the DoT server and get the response
    response_data = await forward_to_dot(data)

    # Send the response back to the client
    udp_server.sendto(response_data, addr)

async def start_tcp_server():
    """Start the TCP server for DNS proxy."""
    server = await asyncio.start_server(handle_tcp_client, '0.0.0.0', PROXY_TCP_PORT)
    addr = server.sockets[0].getsockname()
    print(f"TCP DNS Proxy running on {addr}")

    async with server:
        await server.serve_forever()

async def start_udp_server():
    """Start the UDP server for DNS proxy."""
    loop = asyncio.get_running_loop()

    # Create a datagram socket
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind(('0.0.0.0', PROXY_UDP_PORT))
    udp_server.setblocking(False)

    print(f"UDP DNS Proxy running on 0.0.0.0:{PROXY_UDP_PORT}")

    while True:
        data, addr = await loop.sock_recvfrom(udp_server, BUFFER_SIZE)
        asyncio.create_task(handle_udp_client(data, addr, udp_server))

async def main():
    # Start both TCP and UDP servers concurrently
    await asyncio.gather(
        start_tcp_server(),
        start_udp_server(),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Proxy shut down.")
