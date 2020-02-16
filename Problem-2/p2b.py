import io
import hashlib
import multiprocessing
import threading
from itertools import combinations


class p2:
    def __init__(self):
        self.shadowA = self.readShadow("../Problem-2/SaltedPassTable.txt")
        self.words = "../Problem-2/words.txt"
        self.main()

    def main(self):
        self.part1()
        print("Part 1 finished.")

        self.part2()
        print("Part 2 finished.")

        self.part3()
        print("Part 3 finished.")

        self.part4()
        print("Part 4 finished.")

    @staticmethod
    def readShadow(filename):
        file = io.open(filename, "r")
        pws = {}
        for line in file:
            pws[line.split(':')[0]] = line.split(':')[1] + line.split(':')[2]
        file.close()

        return pws

    # Determines whether a user's password was cracked already
    @staticmethod
    def checkOutput(usr):
        f = open("../Problem-2/output2.txt", "r")
        for c in f:
            if usr == c.split(':')[0].strip(' '):
                return True
        return False

    # Checks common words against hash
    def part1(self):
        for usr in self.shadowA:
            if self.checkOutput(usr):
                continue

            f = open(self.words, "r")
            output = open("../Problem-2/output2.txt", "a+")

            # For all words, tries to hash them with md5
            for word in f:
                word = word.strip('\n')
                if hashlib.md5((self.shadowA.get(usr)[0:8] + word).encode('utf-8')).hexdigest() ==\
                        self.shadowA.get(usr)[8:40].strip('\n'):
                    print(usr + ":" + word)
                    output.write(usr + ":" + word + '\n')
                    break
            f.close()
            output.close()

    def part2(self):
        # Completing section 2 by using processors to decrease time of execution
        t1 = multiprocessing.Process(target=processor, args=(self.shadowA, 1, None))
        t2 = multiprocessing.Process(target=processor, args=(self.shadowA, 2, None))
        t3 = multiprocessing.Process(target=processor, args=(self.shadowA, 3, None))
        t4 = multiprocessing.Process(target=processor, args=(self.shadowA, 4, None))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    def part3(self):
        for usr in self.shadowA:
            if self.checkOutput(usr):
                continue

            output = open("../Problem-2/output2.txt", "a+")
            f = open(self.words, "r")

            print("Working on " + usr)

            for word in f:
                found = False
                word = word.strip('\n')
                space = 10 - len(word)

                if space <= 0:
                    continue

                # Finds the length between a word and 10-digit limit, then computes all numbers from 0 to the max
                # possible within the length, each time comparing the current user to that computed word + number
                # combination
                i = 0
                while (len(str(i)) < space) or not str(i).startswith('9') or not str(i).endswith('9'):
                    if hashlib.md5((self.shadowA.get(usr)[0:8] + (word + str(i))).encode('utf-8')).hexdigest() == \
                            self.shadowA.get(usr)[8:40].strip('\n'):
                        print(usr + ":" + (word+str(i)))
                        output.write(usr + ":" + (word + str(i)) + '\n')
                        found = True
                        break

                    i += 1
                if found:
                    break

            output.close()
            f.close()

    def part4(self):
        f = open(self.words, "r")
        words = []

        for word in f:
            words.append(word.strip('\n'))

        f.close()
        print("Computing possible combinations of words from file...")
        comb = list(combinations(words, 2))
        print("Finished computing possible combinations")

        # Due to the millions of computations needed, I break the task into 3 processes with multiple threads
        # to reduce actual computation time.
        t1 = multiprocessing.Process(target=processor, args=(self.shadowA, 5, comb))
        t2 = multiprocessing.Process(target=processor, args=(self.shadowA, 6, comb))
        t3 = multiprocessing.Process(target=processor, args=(self.shadowA, 7, comb))

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()


# Function that spawns threads under processes, which help reduce compute time. Each thread is in charge of computing
# a pre-defined range, based on the r value (specific value that maps to a certain range and part)
def processor(shadow, r, comb):
    t1 = None
    t2 = None
    t3 = None

    if r == 1:
        t1 = threading.Thread(target=part2h, args=(shadow, range(0, 9999999)))
        t2 = threading.Thread(target=part2h, args=(shadow, range(10000000, 19999999)))
        t3 = threading.Thread(target=part2h, args=(shadow, range(20000000, 29999999)))
    elif r == 2:
        t1 = threading.Thread(target=part2h, args=(shadow, range(30000000, 39999999)))
        t2 = threading.Thread(target=part2h, args=(shadow, range(40000000, 49999999)))
        t3 = threading.Thread(target=part2h, args=(shadow, range(50000000, 59999999)))
    elif r == 3:
        t1 = threading.Thread(target=part2h, args=(shadow, range(60000000, 69999999)))
        t2 = threading.Thread(target=part2h, args=(shadow, range(70000000, 79999999)))
        t3 = threading.Thread(target=part2h, args=(shadow, range(80000000, 89999999)))
    elif r == 4:
        t1 = threading.Thread(target=part2h, args=(shadow, range(90000000, 99999999)))
    elif r == 5:
        t1 = threading.Thread(target=part4h, args=(shadow, comb, 0, 9999999))
        t2 = threading.Thread(target=part4h, args=(shadow, comb, 10000000, 19999999))
    elif r == 6:
        t1 = threading.Thread(target=part4h, args=(shadow, comb, 20000000, 29999999))
        t2 = threading.Thread(target=part4h, args=(shadow, comb, 30000000, 39999999))
    elif r == 7:
        t1 = threading.Thread(target=part4h, args=(shadow, comb, 40000000, 49995000))

    t1.start()

    if r < 4:
        t2.start()
        t3.start()
        t2.join()
        t3.join()

    if 4 < r < 7:
        t2.start()
        t2.join()

    t1.join()


# Function that handles computing of part 2. It loops over a specific range of numbers and compares the numbers to
# user password's hash.
def part2h(shadow, r):
    for usr in shadow:
        if p2.checkOutput(usr):
            continue

        output = open("../Problem-2/output2.txt", "a+")

        print("Working on " + usr)
        for i in r:
            if hashlib.md5((shadow.get(usr)[0:8] + str(i)).encode('utf-8')).hexdigest() == \
                    shadow.get(usr)[8:40].strip('\n'):
                print(usr + ":" + str(i))
                output.write(usr + ":" + str(i) + '\n')
                break

        output.close()


# Function that handles computing of part 4. It loops over a range of possible combinations of concatenated english
# words from the word file.
def part4h(shadow, comb, b, t):
    for usr in shadow:
        if p2.checkOutput(usr):
            continue

        output = open("../Problem-2/output2.txt", "a+")

        # This actually loops through the given range, and computes the forwards and backwards combination
        print("Working on " + usr)
        for c in comb[b:t]:
            if hashlib.md5((shadow.get(usr)[0:8] + (c[0] + c[1])).encode('utf-8')).hexdigest() == \
                    shadow.get(usr)[8:40].strip('\n'):
                print(usr + ":" + (c[0] + c[1]))
                output.write(usr + ":" + (c[0] + c[1]) + '\n')
                break

            if hashlib.md5((shadow.get(usr)[0:8] + (c[1] + c[0])).encode('utf-8')).hexdigest() == \
                    shadow.get(usr)[8:40].strip('\n'):
                print(usr + ":" + (c[1] + c[0]))
                output.write(usr + ":" + (c[1] + c[0]) + '\n')
                break
        output.close()


if __name__ == '__main__':
    p2()
