# -*- coding: UTF-8 -*-
'''
HIll cipher
'''

import numpy


class PlainText:
    __text = ''

    def __init__(self, string):
        isinstance(string, str)
        self.__text = string

    def clear_text(self):
        self.__text = " "

    def set_text(self, str):
        self.__init__(str)

    def get_text(self):
        return self.__text

    def text_padding(self, baseLen, paddingItem=" "):
        isinstance(paddingItem, str)
        while len(self.__text) % baseLen != 0:
            self.__text += paddingItem

    def text_inv_padding(self):
        for i in range(len(self.__text), 0, -1):
            if self.__text[i - 1] != " ":
                self.__text = self.__text[:i]
                break

    def words_to_number(self, base=0):
        '''
        转换为字母序号，A/a=>0，B/b=>1
        base 为基数，默认 base 为 0 ，当 base 为 1 时，A/a=>1，B/b=>2
        '''
        out = []
        text = self.__text.lower()
        for l in text:
            if l.isalpha():
                out.append(ord(l) - 97 + base)
            else:
                out.append(-1)
        return out

    def ascii_to_list(self):
        out = []
        for l in self.__text:
            out.append(ord(l))
        return out

    @staticmethod
    def split_list(_list, length):
        isinstance(_list, list)
        if len(_list) % length != 0:
            raise TypeError
        out = []
        for i in range(int(len(_list) / length)):
            out.append(_list[:length])
            _list = _list[length:]
        return out

    @staticmethod
    def combine_list(_list, level):
        out = []
        for low in _list:
            out += low
        if level != 2:
            PlainText.combine_list(out, level - 1)
        else:
            return out

    @staticmethod
    def number_to_words(_list, base=0):
        out = ''
        for index in _list:
            out += chr(index + 97 - base)
        return out


class Hill:
    __plainText = []
    __key = []

    def __init__(self, plainText, key):
        if not (Hill.check_ok):
            raise TypeError
        self.__plainText = plainText
        self.__key = key

    @staticmethod
    def check_ok(plainText, key):
        keyCol = len(key[0])
        textRow = len(plainText[0])
        return (True if keyCol == textRow else False)

    def encipher(self):
        key = numpy.array(self.__key)
        out = []
        for textGroup in self.__plainText:
            text = numpy.array(textGroup).reshape(-1, 1)
            out += numpy.ndarray.tolist(numpy.transpose(numpy.matmul(key, text) % 26))
        return out

    def decipher(self):
        keyInv = CipherMath.key_inverse(self.__key, 26)
        out = []
        for textGroup in self.__plainText:
            text = numpy.array(textGroup).reshape(-1, 1)
            out += numpy.ndarray.tolist(numpy.transpose(numpy.matmul(keyInv, text) % 26))
        return out


class CipherMath:
    @staticmethod
    def key_inverse(keyList, limit):
        '''
        伴随矩阵法求矩阵逆运算
        '''
        keyArray=numpy.array(keyList)
        keyArrayDet=numpy.linalg.det(keyArray)
        keyArrayInv=numpy.linalg.inv(keyArray)
        keyArrayAdj=numpy.int32(keyArrayInv*keyArrayDet)
        keyArrayInv=keyArrayAdj*CipherMath.get_prime(int(keyArrayDet),26)
        keyArrayInv=keyArrayInv%26
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


MESSAGE = "ukixukydromeiwszxwiokunukhxhroajroanqyebxfzxgc"
SECRET = "meetmeattheusualplaceattenratherthaneightclock"
KEY = [[9, 4], [5, 7]]
KEY_INV = [[5, 12], [15, 25]]

if __name__ == "__main__":
    print("------加密------")
    print("明文：" + MESSAGE)
    pt = PlainText(MESSAGE)
    number = pt.words_to_number()
    splitList = PlainText.split_list(number, 2)

    hill = Hill(splitList, KEY)
    secret = hill.encipher()
    secret = PlainText.combine_list(secret, 2)
    secret = PlainText.number_to_words(secret)
    print("密文：" + secret)

    print("------密文------")
    message=hill.decipher()
    message=PlainText.combine_list(message,2)
    message=PlainText.number_to_words(message)
    print("明文：" + message)