import multiprocessing

def print_cube(num):
    print("Cube: {}".format(num*num*num))

def print_square(num):
    print("Square: {}".format(num*num))


if __name__ == "__main__":
    # arg=(10,) create tuple (immutable - cannot change nor append)
    p1 = multiprocessing.Process(target=print_cube, args=(10,))
    p2 = multiprocessing.Process(target=print_square, args=(10,))

    # start process
    p1.start()
    p2.start()

    # end process
    p1.join()
    p2.join()

    print("Done!")