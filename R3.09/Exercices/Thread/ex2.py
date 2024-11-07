import threading, time

def thread(i, cd):
    for x in range(cd, 0, -1):
        print(f"thread {i} : {cd}")
        time.sleep(1)
        cd -= 1

lThread = []

for i in range(1,3):
    cd = int(input(f"CD du thread {i} : "))
    t = threading.Thread(target=thread, args=(i,cd))
    t.start()
    lThread.append(t)

for t in lThread:
    t.join()