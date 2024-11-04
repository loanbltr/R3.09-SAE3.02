import time, threading

def task(i):
    print(f"Je suis la thread {i}.")

T = []

for i in range(5):
    T.append(threading.Thread(target=task, args=[i]))
print(T)