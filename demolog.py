import http.server
import csv
from urllib.parse import urlparse, parse_qs

# Function to log request data to CSV
def log_request(request_data):
    with open('request_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(request_data)

# HTTP request handler class
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Extract relevant information from the request
        duration = 0  # Placeholder value
        protocol_type = 'TCP' if parsed_url.scheme.lower() == 'http' else 'UDP'  # Get protocol type
        service = parsed_url.path if parsed_url.path else '/'  # Get service
        flag = ''  # Placeholder value
        src_bytes = 0  # Placeholder value
        dst_bytes = 0  # Placeholder value
        land = 0
        wrong_fragment = 0
        urgent = 0
        hot = 0
        num_failed_logins = 0
        logged_in = 0
        num_compromised = 0
        root_shell = 0
        su_attempted = 0
        num_root = 0
        num_file_creations = 0
        num_shells = 0
        num_access_files = 0
        num_outbound_cmds = 0
        is_host_login = 0
        is_guest_login = 0
        count = 0
        srv_count = 0
        serror_rate = 0
        srv_serror_rate = 0
        rerror_rate = 0
        srv_rerror_rate = 0
        same_srv_rate = 0
        diff_srv_rate = 0
        srv_diff_host_rate = 0
        dst_host_count = 0
        dst_host_srv_count = 0
        dst_host_same_srv_rate = 0
        dst_host_diff_srv_rate = 0
        dst_host_same_src_port_rate = 0
        dst_host_srv_diff_host_rate = 0
        dst_host_serror_rate = 0
        dst_host_srv_serror_rate = 0
        dst_host_rerror_rate = 0
        dst_host_srv_rerror_rate = 0

        # Create a list with the request data in the desired format
        request_data = [
            duration, protocol_type, service, flag, src_bytes, dst_bytes, land, wrong_fragment,
            urgent, hot, num_failed_logins, logged_in, num_compromised, root_shell, su_attempted,
            num_root, num_file_creations, num_shells, num_access_files, num_outbound_cmds,
            is_host_login, is_guest_login, count, srv_count, serror_rate, srv_serror_rate,
            rerror_rate, srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate,
            dst_host_count, dst_host_srv_count, dst_host_same_srv_rate, dst_host_diff_srv_rate,
            dst_host_same_src_port_rate, dst_host_srv_diff_host_rate, dst_host_serror_rate,
            dst_host_srv_serror_rate, dst_host_rerror_rate, dst_host_srv_rerror_rate
        ]

        # Log the request data
        log_request(request_data)

        # Read index.html file
        with open('./DemoSight/index.html') as html_file:
            html_content = html_file.read()

        # Send HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

# Run the HTTP server
def run_server(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    # Add column headings as the first line in the CSV file
    with open('request_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land',
            'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
            'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count',
            'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
            'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
            'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
        ])

    run_server()
