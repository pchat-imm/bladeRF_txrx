import multiprocessing

# Result(in process p1): [1, 4, 9, 16]
# Sum of squares(in process p1): 30
# Result(in main program): [1, 4, 9, 16]
# Sum of squares(in main program): 30

def process1(mylist, result, square_sum):
    """
    function to sqaure a given list
    """
    # append squares of mylist to result array
    # enumerate to take care of index and val without index yourself
    for idx, num in enumerate(mylist):
        result[idx] = num * num
    
    # square_sum value
    square_sum.value = sum(result)

    print("Result(in process p1): {}".format(result[:]))
    print("Sum of squares(in process p1): {}". format(square_sum.value))

if __name__ == "__main__":
    mylist = [1,2,3,4]

    # result array of integer of 4
    result = multiprocessing.Array('i', 4)
    square_sum = multiprocessing.Value('i')

    p1 = multiprocessing.Process(target=process1, args=(mylist, result, square_sum))
    p1.start()
    p1.join()

    print("Result(in main process): {}".format(result[:]))
    print("Sum of sqaures(in main process): {}".format(square_sum.value))


## result
# Result(in process p1): [1, 4, 9, 16]
# Sum of squares(in process p1): 30
# Result(in main process): [1, 4, 9, 16]
# Sum of sqaures(in main process): 30