import socket
from Seq1 import Seq
from Seq1 import Color

def PING():
    print(f"{Color.GREEN} PING command! {Color.END}")
    response = "OK!\n"
    return response

def GET(msg):
    print(f"{Color.GREEN} GET {Color.END}")
    index = int(msg[4])
    seq_l = ["ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA\n", "AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA\n", "CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT\n", "CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA\n", "AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT\n"]
    return seq_l[index]

def INFO(seq):
    seq = Seq(seq)
    bases_dict = seq.seq_count()
    len = seq.seq_len()
    solution = ""

    for key, number in bases_dict.items():
        solution += f"{key}: {number} ({round(number/len*100, 1)}%)\n"

    return solution


def main():
    IP = "127.0.0.1"
    PORT = 8080

    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind((IP, PORT))
    ls.listen()

    while True:
        print("Waiting for connections at {}, {}".format(IP, PORT) + "\n")

        try:
            (rs, address) = ls.accept()
        except KeyboardInterrupt:
            print("Server stopped")
            ls.close()
            exit()

        else:
            print('A client has connected')

            msg = str(rs.recv(2048).decode("utf-8"))

            if msg == "PING":
                response = PING()
                rs.send(response.encode())
                print(response)

            elif msg[:3] == "GET" and int(msg[4]) in [0, 1, 2, 3, 4]:
                response = GET(msg)
                rs.send(response.encode())
                print(response)

            elif "INFO" in msg:
                print(f"{Color.GREEN}INFO{Color.END}")
                seq = (msg.split())[1]
                s1 = Seq(seq)
                print("Sequence:", seq)
                print("Total length:", s1.seq_len())
                response = INFO(seq)
                print(response)
                rs.send(response.encode())

            elif "COMP" in msg:
                print(f"{Color.GREEN}COMP{Color.END}")
                seq = (msg.split())[1]
                s1 = Seq(seq)
                response = s1.seq_complement()
                print(response)
                rs.send(response.encode())

            elif "REV" in msg:
                print(f"{Color.GREEN}REV{Color.END}")
                seq = (msg.split())[1]
                s1 = Seq(seq)
                response = s1.seq_reverse() + "\n"
                print(response)
                rs.send(response.encode())

            elif "GENE" in msg:
                print(f"{Color.GREEN}GENE{Color.END}")
                file = (msg.split())[1]
                file = "../sequences/" + file + ".txt"
                seq = Seq()
                seq.seq_read_fasta(file)
                seq = str(seq)
                print(seq)
                rs.send(seq.encode())

            else:
                msg = "Unexpected command \n"
                print(msg)
                rs.send(msg.encode())

            rs.close()

if __name__ == "__main__":
    main()