import http.server
import socketserver
import termcolor
from Seq1 import *
import jinja2 as j
from urllib.parse import parse_qs, urlparse
from pathlib import Path

IP = "127.0.0.1"
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents
class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green',force_color=True)

        files = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
        numbers = ["0", "1", "2", "3", "4"]
        operations = ["op=info", "op=comp", "op=rev"]

        command = self.requestline.split(" ")[1].replace("/info", "").replace(".html", "")

        if command == "/" or command == "/index":
            contents = open("html/index.html", "r").read()

        elif command == "/ping?":
            contents = open("html/ping.html", "r").read()

        elif command.startswith("/get?seq=") and command.replace("/get?seq=", "") in numbers:
            n = int(command.split("=")[1])
            seq_name = files[n]
            s = Seq()
            seq = s.seq_read_fasta("../sequences/" + seq_name + ".txt")
            contents = read_html_file("get.html").render(context={"todisplay": n, "todisplay2": seq})

        elif command.startswith("/gene?seq=") and command.replace("/gene?seq=", "") in files:
            seq_name = command.replace("/gene?seq=", "")
            s = Seq()
            seq = s.seq_read_fasta_2("../sequences/" + seq_name + ".txt")
            contents = read_html_file("gene.html").render(context={"todisplay": seq_name, "todisplay2": seq})

        elif command.startswith("/operation?seq=") and command.replace("/operation?seq=", "").split("&")[1] in operations:
            seq = command.replace("/operation?seq=", "").split("&")[0]
            operation = command.replace("/operation?seq=", "").split("&")[1]
            operation = operation.replace("op=", "")

            s = Seq(seq)

            if operation == "info":
                result = "Total length: " + str(len(seq)) + "<br><br>"
                bases_dict = s.seq_count()

                if len(seq) != 0:
                    for e in bases_dict:
                         result += e + ": " + str(bases_dict[e]) + " (" + str(round((bases_dict[e] / len(seq) * 100), 1)) + "%" + ")" +  "<br><br>"

            elif operation == "comp":
                result = s.seq_complement()
            elif operation == "rev":
                result = s.seq_reverse()

            contents = read_html_file("operation.html").render(context={"todisplay": seq, "todisplay2": operation, "todisplay3": result})

        else:
            contents = open("html/error.html", "r").read()

        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))

        self.end_headers()

        self.wfile.write(contents.encode())

        return

Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()