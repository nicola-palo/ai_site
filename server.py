#!/usr/bin/env python3
"""
Simple HTTP server with CORS support for testing AI context access
"""

import http.server
import socketserver
import json
from pathlib import Path

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS headers."""
    
    def end_headers(self):
        """Add CORS headers to every response."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Set correct content type for JSON files
        if self.path.endswith('.json'):
            self.send_header('Content-Type', 'application/json')
        
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight requests."""
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        """Override GET to add special handling for AI queries."""
        
        # Intercept special AI query endpoints
        if self.path.startswith('/api/search?'):
            self.handle_search_request()
        elif self.path.startswith('/api/metadata'):
            self.handle_metadata_request()
        else:
            # Default file serving
            super().do_GET()
    
    def handle_search_request(self):
        """Handle semantic search requests from AI."""
        try:
            # Parse query parameters
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            query = params.get('q', [''])[0]
            top_k = int(params.get('topK', [5])[0])
            
            # Load JSON data
            with open('ai-context.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Simple text search (in production, use vector similarity)
            results = []
            for doc in data['documents']:
                if query.lower() in doc['content'].lower():
                    results.append({
                        'id': doc['id'],
                        'page': doc['page'],
                        'content': doc['content'],
                        'snippet': doc['content'][:200] + '...'
                    })
                    if len(results) >= top_k:
                        break
            
            response = {
                'query': query,
                'results': results,
                'total': len(results)
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_metadata_request(self):
        """Handle metadata requests from AI."""
        try:
            with open('ai-context.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            response = {
                'metadata': data['metadata'],
                'instructions': data['instructions'],
                'document_count': len(data.get('documents', []))
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))

def main():
    PORT = 8080
    
    print(f"Starting server on http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    print("\nAI-readable endpoints:")
    print(f"  - http://localhost:{PORT}/               (Main page)")
    print(f"  - http://localhost:{PORT}/ai-context.json (Full dataset)")
    print(f"  - http://localhost:{PORT}/api/metadata    (Dataset metadata)")
    print(f"  - http://localhost:{PORT}/api/search?q=query&topK=5 (Search)")
    
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()