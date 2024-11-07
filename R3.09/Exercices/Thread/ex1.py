import time, threading

def threads(i):
    for x in range(5):
        print(f"Je suis la thread {i}")
        time.sleep(1)

lThread = []

for i in range(1, 3):
    t = threading.Thread(target=threads, args=[i])
    t.start()
    lThread.append(t)

for t in lThread:
    t.join()