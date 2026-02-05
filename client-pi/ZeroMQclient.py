import zmq
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.getenv('SERVER_IP', 'localhost')
SERVER_PORT = os.getenv('SERVER_PORT', '5555')

context = zmq.Context()

print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}…")
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{SERVER_IP}:{SERVER_PORT}")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print(f"Sending request {request} …")
    socket.send(b"Hello")

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")