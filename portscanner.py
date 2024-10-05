import sys
import socket
import time
import datetime
import threading

from queue import Queue
socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()
open_ports = []
scan_results = open("results.txt", "w+")
hostname = input("Enter a host to scan ")
try:
    host = socket.gethostbyname(hostname)
except socket.gaierror:
    print("INVALID HOST NAME", file=open("results.txt", "a"))
    sys.exit()
else:
    print("Beginning scan on " + host, file=open("results.txt", "a"))


def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((host, port))
        with print_lock:
            open_ports.append(port)
            con.close()
    except:
        pass


def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()


q = Queue()
startTime = time.time()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(1, 1026):
    q.put(worker)

q.join()
totalTime = time.time() - startTime
print("OPEN PORTS:", file=open("results.txt", "a"))
for port in open_ports:
    print(port, file=open("results.txt", "a"))
print(datetime.datetime.now(), file=open("results.txt", "a"))
print(totalTime, file=open("results.txt", "a"))
scan_results.close()
