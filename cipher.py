import util
import numpy as np

# __all__ = ["Hill", "Des"]


class Hill:
    __key = [[]]
    __content = [[]]

    def __init__(self, content=[[]], key=[[]]):
        self.__content = content  ## BlockArray
        self.__key = key  ## BlockArray

    def set_key(self, key):
        self.__key = key

    def reset_key(self):
        self.__key = [[]]

    def put_key(self, isPrint=False):
        if self.__key != [[]]:
            if isPrint:
                print("希尔密码密钥：")
                for line in self.__key:
                    print(line)
            return self.__key
        else:
            print("Warning: 对象没有密钥")

    def set_content(self, content):
        pass

    def reset_content(self):
        self.__content = [[]]

    def put_content(self, isPrint=False):
        self.put_key(isPrint)

    def generate_hill_key_block(self, keyLen, keySapce=256, method=""):
        if np.sqrt(keyLen) != int(np.sqrt(keyLen)):
            keyLen = (int(np.sqrt(keyLen) + 1)) * (int(np.sqrt(keyLen) + 1))
            print("希尔密码密钥长度重置为" + str(keyLen))
        rowLen = int(np.sqrt(keyLen))
        keyBlock = []
        keyLine = []
        while 1:
            for i in range(0, rowLen):
                for j in range(0, rowLen):
                    keyLine.append(np.random.randint(0, 255))
                keyBlock.append(keyLine)
                keyLine = []
            if np.linalg.det(np.array(keyBlock)) != 0:
                break
            keyBlock = []  # 非可逆矩阵，清除
        if method == "return":
            return keyBlock
        self.__key = keyBlock

    def generate_hill_key_block_array(self, keyLen, blockNum, keySapce=256, method=""):
        keyBlockArray = []
        for num in range(blockNum):
            keyBlockArray.append(self.generate_hill_key_block(keyLen, method="return"))
        if method == "return":
            return keyBlockArray
        self.__key = keyBlockArray

    def encrypt(self, field, **arg):
        cipherBlockArray = Hill.encrypt_block_array(self.__content, self.__key, 256)
        return cipherBlockArray

    def decrypt(self, fied, **arg):
        plainBlockArray = Hill.decrypt_block_array(self.__content, self.__key, 256)
        return plainBlockArray

    @staticmethod
    def encrypt_block_array(contentBlockArray, keyBlockArray, field, multiKeyEncryption=False, **arg):
        cipherBlockArray = []
        keyBlockNum = 0
        if multiKeyEncryption:
            for contentBlock in contentBlockArray:
                outMetrix = Hill.encrypt_block(contentBlock, keyBlockArray[keyBlockNum % len(keyBlockArray)], field)
                cipherBlockArray.append(outMetrix)
                keyBlockNum += 1
        else:
            for contentBlock in contentBlockArray:
                outMetrix = Hill.encrypt_block(contentBlock, keyBlockArray[0], field)
                cipherBlockArray.append(outMetrix)
        return cipherBlockArray

    @staticmethod
    def decrypt_block_array(contentBlockArray, keyBlock, field):
        plainBlockArray = []
        for contentBlock in contentBlockArray:
            outMetrix = Hill.decrypt_block(contentBlock, keyBlock, field)
        plainBlockArray.append(outMetrix)
        return plainBlockArray

    # 希尔密码 Block 处理
    @staticmethod
    def encrypt_block(contentBlock, keyBlock, field):
        cipherBlock = []
        contentArray = np.array(contentBlock)
        keyArray = np.array(keyBlock)
        cipherBlock = np.ndarray.tolist(contentArray * keyArray)
        cipherBlock = np.ndarray.tolist(np.array(cipherBlock) % (field))
        return cipherBlock

    @staticmethod
    def decrypt_block(contentBlock, keyBlock, field):
        plainBlock = []
        contentArray = np.array(contentBlock)
        keyArray = np.array(keyBlock)
        plainBlock = np.ndarray.tolist(contentArray * np.linalg.inv(keyArray))
        plainBlock = np.ndarray.tolist(np.array(plainBlock) % (field))
        return plainBlock


class Des:

    # 常量部分
    # yapf: disable

    # P 盒
    IP   = [[58, 50, 42, 34, 26, 18, 10, 2],
            [60, 52, 44, 36, 28, 20, 12, 4],
            [62, 54, 46, 38, 30, 22, 14, 6],
            [64, 56, 48, 40, 32, 24, 16, 8],
            [57, 49, 41, 33, 25, 17,  9, 1],
            [59, 51, 43, 35, 27, 19, 11, 3],
            [61, 53, 45, 37, 29, 21, 13, 5],
            [63, 55, 47, 39, 31, 23, 15, 7]]

    # P 盒逆
    IP_INV = []

    # S 盒
    S_BOX = [
            [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
            ],
            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
            ],
            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
            ],
            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
            ],
            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
            ],
            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
            ],
            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
            ],
            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
            ]
            ]

    # yapf: disable

    def __init__(self):
        self.algorithm="DES"

    def set_name(self,nn):
        self.name =nn

    def print(self):
        print("name is:"+self.name)

# if __name__ == "__main__":
#     a=Hill()
#     a.generate_hill_key(64)
#     a.put_key(True)