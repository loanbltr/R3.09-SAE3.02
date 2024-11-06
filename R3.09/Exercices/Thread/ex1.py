import time, threading

def task(i):
    for x in range(5):
        print(f'je suis le thread {i}')
        time.sleep(1)

myThreads: list[threading.Thread] = []
for i in range(1, 3):
    t = threading.Thread(target=task, args=[i])
    t.start()
    myThreads.append(t)

for t in myThreads:
    t.join()