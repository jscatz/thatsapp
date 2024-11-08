import asyncio
import websockets
import json
import base64

# Server information
HOST = input("HOST: ")
PORT = 9009

# List to store all connected clients and nicknames
clients = set()
nicknames = {}

# Function to broadcast messages to all clients
async def broadcast(message):
    if clients:  # Only broadcast if there are clients connected
        await asyncio.wait([client.send(message) for client in clients])

# Function to handle individual client connections
async def handle_client(websocket, path):
    # Receive the nickname
    await websocket.send("NICK")
    nickname = await websocket.recv()
    nicknames[websocket] = nickname
    clients.add(websocket)

    # Notify all clients about the new connection
    await broadcast(json.dumps({"type": "text", "content": f"{nickname} has joined the chat!"}))

    try:
        # Listen for messages from the client
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'text':
                # Broadcast text message
                await broadcast(json.dumps({
                    "type": "text",
                    "content": f"{nickname}: {data['content']}"
                }))
            elif data['type'] == 'file':
                # Broadcast file message
                await broadcast(json.dumps({
                    "type": "file",
                    "filename": data['filename'],
                    "content": data['content']
                }))
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection with {nickname} closed: {e}")
    finally:
        # Remove the client from the list and notify others
        clients.remove(websocket)
        await broadcast(json.dumps({"type": "text", "content": f"{nickname} has left the chat!"}))
        nicknames.pop(websocket, None)

# Main function to start the server
async def main():
    print("Starting WebSocket server...")
    async with websockets.serve(handle_client, HOST, PORT):
        print(f"Server is listening on {HOST}:{PORT}")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
