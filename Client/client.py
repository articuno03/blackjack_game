import socket
import sys
import types
import selectors

sel = selectors.DefaultSelector()

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        conn_id = i + 1
        print("starting connection", conn_id, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False) # non-blocking connection for asynchronous activity
        try:
            sock.connect_ex(server_addr)
        except BlockingIOError:
            pass # Connection is in progress
        data = types.SimpleNamespace( # Stores relevant connection data
            conn_id = conn_id,
            recv_total = 0,
            outb=b"",
            messages = ["Hello from client {conn_id}!".encode()] # Example message
            msg_total = 1 # Total messages to send
        )
        sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) # Read
        if recv_data:
            print("received", repr(recv_data), "from connection", data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("sending", repr(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb)  # Write
            data.outb = data.outb[sent:]


# Main

host = ''   # use 0.0.0.0 if you want to communicate across machines in a real network
port = 65432
num_conns = 10       # number of clients (change as needed)


start_connections(host, port, num_conns)


# Event

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()


