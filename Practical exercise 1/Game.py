import socket
import random

class NumberGuesser:
    def __init__(self, secret_number, attempts):
        self.secret_number = int(secret_number)
        self.attempts = attempts

    def guess(self, number):
        try:
            number = int(number)

            if number == self.secret_number:
                response = f"Congrats, you got the number after {self.attempts} attempts."
            if number < self.secret_number:
                response = "Try a higher number."
            if number > self.secret_number:
                response = "Try a lower number."

        except ValueError:
            response = "Please enter a valid number."


        return response


IP = "212.128.255.79"
PORT = 8080

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()

attempts = 0

secret_number = random.randint(1,100)

while True:
    print("Waiting for connections at {}, {}".format(IP, PORT) + "\n")
    attempts += 1

    try:
        (rs, address) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped")
        ls.close()
        exit()

    else:
        print('A client has connected')

        msg = str(rs.recv(2048).decode("utf-8"))
        print(f"The client attempt is: {msg}")
        c = NumberGuesser(secret_number, attempts)
        response = c.guess(msg)
        rs.send(response.encode())

        if "Congrats" in response:
            print("Server stopped")
            ls.close()
            exit()

        rs.close()