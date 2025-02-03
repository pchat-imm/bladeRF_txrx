import multiprocessing
import os

def task1():
# ID of process running worker1: 29305
    print("ID of process running worker1: {}".format(os.getpid()))    

def task2():
    print("ID of process running worker2: {}".format(os.getpid()))   

if __name__ == "__main__":
    print("ID of main process: {}".format(os.getpid()))

    # create process
    p1 = multiprocessing.Process(target=task1)
    p2 = multiprocessing.Process(target=task2)

    # start process
    p1.start()
    p2.start()
    print("ID of process p1: {}".format(p1.pid))
    print("ID of process p2: {}".format(p2.pid))

    # end process
    p1.join()
    p2.join()
    print("Both processes finished execution!")

    # check process is_alive
    print("Process p1 is alive: {}".format(p1.is_alive()))
    print("Process p2 is alive: {}".format(p2.is_alive()))

## result
# ID of main process: 8384
# ID of process p1: 8385
# ID of process p2: 8386
# ID of process running worker1: 8385
# ID of process running worker2: 8386
# Both processes finished execution!
# Process p1 is alive: False
# Process p2 is alive: False