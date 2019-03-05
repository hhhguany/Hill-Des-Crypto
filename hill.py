# -*- coding: UTF-8 -*-
'''
HIll cipher
'''

import numpy
import util


class PlainText:
    __text = []
    __groupLen = 0

    def __init__(self, string, groupLen):
        isinstance(string, str)
        try:
            if groupLen > 0:
                self.__text = string
                self.__groupLen = groupLen
            else:
                raise TypeError
        except TypeError as e:
            print(e)

    def clear_text(self):
        self.__text = " "

    def set_text(self, str):
        self.__init__(str)

    def get_text(self):
        return self.__text

    def encode_text(self, encode=0):
        ENCODE = ["number0", "number1", "ASCII"]
        if encode == 0:
            text = util.StringOpt.words_to_number(self.__text)
        elif encode == 1:
            text = util.StringOpt.words_to_number(self.__text, 1)
        elif encode == 2:
            text = util.StringOpt.ascii_to_list(self.__text)
        else:
            raise TypeError
        text = util.StringOpt.split_list(text, self.__groupLen)
        return text

class Hill:
    __plainText = []
    __secret=[]
    __key = []

    def __init__(self, key):
        isinstance(key,list)
        self.__key = key
    
    def set_plainText(self,text):
        pt=PlainText(text,len(self.__key))
        self.__plainText=pt.encode_text()
    
    def set_secret(self,secret):
        pt=PlainText(secret,len(self.__key))
        self.__secret=pt.encode_text()

    @staticmethod
    def check_ok(text, key):
        keyCol = len(key[0])
        textRow = len(text[0])
        if keyCol != textRow:
            raise TypeError

    def encipher(self):
        key = numpy.array(self.__key)
        out = []
        for textGroup in self.__plainText:
            text = numpy.array(textGroup).reshape(-1, 1)
            out += numpy.ndarray.tolist(numpy.transpose(numpy.matmul(key, text) % 26))
        #todo:未正确实现
        out=util.StringOpt.combine_list(out,2)
        out=util.StringOpt.number_to_words(out)
        return out

    def decipher(self):
        keyInv = CipherMath.key_inverse(self.__key, 26)
        out = []
        for textGroup in self.__secret:
            text = numpy.array(textGroup).reshape(-1, 1)
            out += numpy.ndarray.tolist(numpy.transpose(numpy.matmul(keyInv, text) % 26))
        #todo:未正确实现
        out=util.StringOpt.combine_list(out,2)
        out=util.StringOpt.number_to_words(out)
        return out


class CipherMath:
    @staticmethod
    def key_inverse(keyList, limit):
        '''
        伴随矩阵法求矩阵逆运算
        '''
        keyArray = numpy.array(keyList)
        keyArrayDet = numpy.linalg.det(keyArray)
        keyArrayInv = numpy.linalg.inv(keyArray)
        keyArrayAdj = numpy.int32(keyArrayInv * keyArrayDet)
        keyArrayInv = keyArrayAdj * CipherMath.get_prime(int(keyArrayDet), 26)
        keyArrayInv = keyArrayInv % 26
        return keyArrayInv

    @staticmethod
    def get_prime(number, field):
        '''
        用于求 number * result = 1 mod field
        7*8=1 mod 11
        '''
        flag = False
        for k in range(1, field):
            for i in range(field):
                if (i * number) % field == k:
                    flag = True
                    break
            if flag:
                break
        return i


MESSAGE = "meetmeattheusualplaceattenratherthaneightclock"
SECRET = "ukixukydromeiwszxwiokunukhxhroajroanqyebxfzxgc"
KEY = [[9, 4], [5, 7]]
KEY_INV = [[5, 12], [15, 25]]

if __name__ == "__main__":
    print("------加密------")
    print("明文：" + MESSAGE)
    hill=Hill(KEY)
    hill.set_plainText(MESSAGE)

    secret = hill.encipher()
    print("密文：" + secret)

    print("------密文------")
    hill.set_secret(secret)
    message = hill.decipher()
    print("明文：" + message)