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
                out.append(ord(l) - 65 + base)
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
        out=[]
        for low in _list:
            out+=low
        if level!=2:
            PlainText.combine_list(out,level-1)
        else:
            return out

    @staticmethod
    def number_to_words(_list,base=0):
        out=''
        for index in _list:
            out+=chr(index+65-base)
        return out

class Hill:
    __plainText=[]
    __key=[]

    def __init__(self,plainText,key):
        if not(Hill.check_ok):
            raise TypeError
        self.__plainText=plainText
        self.__key=key

    @staticmethod
    def check_ok(plainText,key):
        keyCol=len(key[0])
        textRow=len(plainText[0])
        return (True if keyCol==textRow else False)
            
    def enCipher(self):
        key=numpy.array(self.__key)
        out=[]
        for textGroup in self.__plainText:
            text=numpy.transpose(numpy.array(textGroup))
            out.append(numpy.ndarray.tolist(numpy.transpose(numpy.multiply(key,text)%26)))
        return out



if __name__ == "__main__":
    pt = PlainText("meetmeattheusualplaceattenratherthaneightclock")
    number = pt.words_to_number()
    print(number)
    splitList=PlainText.split_list(number, 2)
    print(splitList)
    keyList=[[9,4],[5,7]]

    hill = Hill(splitList,keyList)
    secret=hill.enCipher()

    print(secret)

    combineList=PlainText.combine_list(splitList,2)
    print(combineList)
    words=PlainText.number_to_words(combineList)
    print(words)

