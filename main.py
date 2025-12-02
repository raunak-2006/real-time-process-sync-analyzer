# Project: Real-Time Process Synchronization Analyzer

import threading
import time

log_messages = []

def log(msg):
    print(msg)
    log_messages.append(msg)


def race_worker(counter, iterations):
    for _ in range(iterations):
        temp = counter["value"]
        temp += 1
        counter["value"] = temp

def run_race_condition(num_threads=5, iterations=100000):
    counter = {"value": 0}
    threads = []

    for i in range(num_threads):
        t = threading.Thread(target=race_worker, args=(counter, iterations), name=f"T{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = num_threads * iterations
    actual = counter["value"]

    log(f"[RACE] Expected = {expected}, Actual = {actual}")
    if actual != expected:
        log("[RACE] Race condition detected! Final value is incorrect.")
    else:
        log("[RACE] No race detected (this is rare but possible).")

# ---------- Synchronized Scenario ----------

def sync_worker(counter, iterations, lock):
    for _ in range(iterations):
        with lock:  
            temp = counter["value"]
            temp += 1
            counter["value"] = temp

def run_synchronized(num_threads=5, iterations=100000):
    counter = {"value": 0}
    lock = threading.Lock()
    threads = []

    for i in range(num_threads):
        t = threading.Thread(target=sync_worker, args=(counter, iterations, lock), name=f"T{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = num_threads * iterations
    actual = counter["value"]

    log(f"[SYNC] Expected = {expected}, Actual = {actual}")
    if actual == expected:
        log("[SYNC] Synchronization successful. No race condition.")
    else:
        log("[SYNC] Something is wrong. Value mismatch even with lock!")


def deadlock_worker_1(lock_a, lock_b):
    thread_name = threading.current_thread().name
    log(f"[{thread_name}] Trying to acquire Lock A")
    with lock_a:
        log(f"[{thread_name}] Acquired Lock A")
        time.sleep(1)
        log(f"[{thread_name}] Trying to acquire Lock B")
        with lock_b:
            log(f"[{thread_name}] Acquired Lock B")

def deadlock_worker_2(lock_a, lock_b):
    thread_name = threading.current_thread().name
    log(f"[{thread_name}] Trying to acquire Lock B")
    with lock_b:
        log(f"[{thread_name}] Acquired Lock B")
        time.sleep(1)
        log(f"[{thread_name}] Trying to acquire Lock A")
        with lock_a:
            log(f"[{thread_name}] Acquired Lock A")

def run_deadlock_demo(timeout=5):
    lock_a = threading.Lock()
    lock_b = threading.Lock()

    t1 = threading.Thread(target=deadlock_worker_1, args=(lock_a, lock_b), name="T1")
    t2 = threading.Thread(target=deadlock_worker_2, args=(lock_a, lock_b), name="T2")

    t1.start()
    t2.start()

    t1.join(timeout)
    t2.join(timeout)

    if t1.is_alive() or t2.is_alive():
        log("[DEADLOCK] Deadlock detected: threads are still waiting for each other.")
    else:
        log("[DEADLOCK] No deadlock occurred (locks were acquired successfully).")


def save_report(filename="report.txt"):
    with open(filename, "w") as f:
        for line in log_messages:
            f.write(line + "\n")
    print(f"\nReport saved to {filename}")

def main_menu():
    while True:
        print("\n==== Real-Time Process Synchronization Analyzer ====")
        print("1. Run Race Condition Scenario (without lock)")
        print("2. Run Synchronized Scenario (with lock)")
        print("3. Run Deadlock Demo")
        print("4. Save Report and Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            run_race_condition()
        elif choice == "2":
            run_synchronized()
        elif choice == "3":
            run_deadlock_demo()
        elif choice == "4":
            save_report()
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()



