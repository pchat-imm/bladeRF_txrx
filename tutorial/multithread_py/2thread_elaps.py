import threading

def print_cube(num):
    print("Cube: {}".format(num*num*num))

def print_square(num):
    print("Square: {}".format(num*num))

# for when is run directly not when import by another script
if __name__ == "__main__":
    # create thread
    # arg=(10,) create tuple (immutable - cannot change nor append)
    t1 = threading.Thread(target=print_cube, args=(10,))
    t2 = threading.Thread(target=print_square, args=(10,))

    # start thread
    t1.start()
    t2.start()

    # end thread
    t1.join()
    t2.join()

    print("Done!")
