import multiprocessing

# empty list with global scope
result = []

def square_list(mylist):
    """
    function to sqaure a given list
    """
    global result
    # append squares of mylist to global list result
    for num in mylist:
        result.append(num * num)
        # print global result
        print("Result(in process p1): {}".format(result))

if __name__ == "__main__":
    # input_list
    mylist = [1,2,3,4]

    # create new process
    p1 = multiprocessing.Process(target=square_list, args=(mylist,))

    p1.start()

    p1.join()

    print("Result (in main program): {}".format(result))

## result
# Result(in process p1): [1]
# Result(in process p1): [1, 4]
# Result(in process p1): [1, 4, 9]
# Result(in process p1): [1, 4, 9, 16]
# Result (in main program): []