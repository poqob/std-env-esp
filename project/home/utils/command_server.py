import machine
import json
import socket
import time
import _thread
import gc

class CommandServer:
    def __init__(self, port=8080, api_key="your_secret_api_key"):
        """
        Starts a command server for ESP32.
        
        Args:
            port (int): The port number to listen on
            api_key (str): API security key
        """
        self.port = port
        self.api_key = api_key
        self.server_socket = None
        self.running = False
        self.routes = {
            '/restart': self.handle_restart
        }

    def start(self):
        """Starts the server and begins listening for connections."""
        try:
            addr = socket.getaddrinfo('0.0.0.0', self.port)[0][-1]
            self.server_socket = socket.socket()
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(addr)
            self.server_socket.listen(5)
            
            print(f"Command server started on port {self.port}")
            self.running = True
            
            # Run server loop in a separate thread
            _thread.start_new_thread(self._server_loop, ())
        except Exception as e:
            print(f"Server start failed: {e}")
            
    def _server_loop(self):
        """Main server loop - listens for connections and processes requests."""
        while self.running:
            try:
                client, addr = self.server_socket.accept()
                print(f'Client connected from {addr}')
                _thread.start_new_thread(self._handle_client, (client, addr))
            except Exception as e:
                print(f"Error accepting connection: {e}")
            
            # Memory management
            gc.collect()
    
    def _handle_client(self, client, addr):
        """Handles client connection."""
        try:
            request = client.recv(1024).decode()
            if not request:
                client.close()
                return
            
            method, path, headers, body = self._parse_request(request)
            print(f"{method} {path}")
            
            # Find the appropriate handler for the requested endpoint
            if path in self.routes and method == 'POST':
                response = self.routes[path](headers, body)
            else:
                response = self._create_response(404, "Not Found")
            
            client.send(response)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client.close()
    
    def _parse_request(self, request):
        """Parses HTTP request."""
        lines = request.split('\r\n')
        
        # Get method and path from the first line
        request_line = lines[0].split(' ')
        method = request_line[0]
        path = request_line[1].split('?')[0]  # ignore query parameters
        
        # Parse headers
        headers = {}
        body_start = 0
        for i, line in enumerate(lines[1:], 1):
            if not line:  # Empty line indicates the end of headers
                body_start = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        # Get the body (if any)
        body = '\r\n'.join(lines[body_start:]) if body_start < len(lines) else ''
        
        return method, path, headers, body
    
    def _create_response(self, status_code, message, content_type="application/json"):
        """Creates HTTP response."""
        status_messages = {
            200: "OK",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error"
        }
        
        status_text = status_messages.get(status_code, "Unknown")
        response = f"HTTP/1.1 {status_code} {status_text}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += "Connection: close\r\n\r\n"
        
        if isinstance(message, dict):
            response += json.dumps(message)
        else:
            response += message
            
        return response.encode()
    
    def handle_restart(self, headers, body):
        """Handler for the '/restart' endpoint."""
        try:
            # Parse JSON data from body
            data = json.loads(body)
            
            # Check API key
            if 'api_key' not in data or data['api_key'] != self.api_key:
                return self._create_response(401, {"error": "Unauthorized: Invalid API key"})
            
            # Send successful response
            response = self._create_response(200, {"message": "Device will restart in 2 seconds"})
            
            # Start restart process after 2 seconds (to allow the response to be sent)
            _thread.start_new_thread(self._delayed_restart, (2,))
            
            return response
            
        except json.JSONDecodeError:
            return self._create_response(400, {"error": "Invalid JSON data"})
        except Exception as e:
            return self._create_response(500, {"error": f"Internal error: {str(e)}"})
    
    def _delayed_restart(self, delay_seconds):
        """Restarts ESP32 after a specified delay."""
        time.sleep(delay_seconds)
        machine.reset()
        
    def stop(self):
        """Stops the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
