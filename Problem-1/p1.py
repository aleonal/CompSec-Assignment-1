import io
import crypt


class p1:
    def __init__(self):
        self.main()

    def main(self):
        info = self.readShadow("../Problem-1/shadowfile.txt")
        self.crackShadow(info, "../Problem-1/commonPasswdFile1.txt", "../Problem-1/commonPasswordFile2.txt")

    @staticmethod
    def readShadow(filename):
        file = io.open(filename, "r")
        pws = {}
        for line in file:
            usr = line.split(':')[0]
            pw = line.split(':')[1]
            pws[usr] = pw

        file.close()
        return pws

    @staticmethod
    def crackShadow(pws, rep1, rep2):
        i = 2

        for k in pws:
            # An true entry must at least be 12 characters, which account for the salt of a password
            if len(pws.get(k)) < 11:
                i -= 1
                continue
            if i > 0:
                i -= 1
                continue

            f1 = open(rep1, "r")
            f2 = open(rep2, "r")

            # Checks both common password files simultaneously
            for clear1, clear2 in zip(f1, f2):
                clear1 = clear1.strip('\n')
                clear2 = clear2.strip('\n')

                result1 = crypt.crypt(clear1, pws.get(k)[0:11])
                result2 = crypt.crypt(clear2, pws.get(k)[0:11])

                if result1 == pws.get(k):
                    print(k + " : " + clear1)
                    break
                if result2 == pws.get(k):
                    print(k + " : " + clear2)
                    break

            f1.close()
            f2.close()

if __name__ == '__main__':
    p1()
