import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class CropXcelHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/health":
			response = {"status": "ok", "service": "CropXcel backend"}
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
		elif self.path == "/":
			response = {"message": "CropXcel backend is running"}
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
		else:
			response = {"error": "Not found"}
			self.send_response(404)
			self.send_header("Content-Type", "application/json")

		body = json.dumps(response).encode("utf-8")
		self.send_header("Content-Length", str(len(body)))
		self.end_headers()
		self.wfile.write(body)


if __name__ == "__main__":
	server = HTTPServer(("127.0.0.1", 8000), CropXcelHandler)
	print("CropXcel backend running at http://127.0.0.1:8000")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("\nStopping CropXcel backend")
	finally:
		server.server_close()
