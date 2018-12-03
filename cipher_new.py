# -*- coding: UTF-8 -*-
import sys, optparse
import numpy as np

## usage:
## python cipher_new.py


def main():
    options = get_args()
    ## test
    # options.function="decrypto"
    # options.inFile="output.txt"
    # options.outFile="1.txt"
    # algorithm = get_algorithm(options)
    # function = get_function(options)
    # cipherText = encrypto(options)
    # print_content(cipherText)
    encrypto(options)

    input()


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--infile", dest="inFile", default="message.txt", type="string", help="明文路径，默认为当前目录下 message.txt 文件")
    parser.add_option("-o", "--outfile", dest="outFile", default="output.txt", type="string", help="输出明文路径，默认输出到当前目录下 output.txt 文件")
    parser.add_option("-d", "--decode", dest="decode", default="ASCII", type="string", help="解码方式：[ASCII]")
    parser.add_option("-e", "--encode", dest="encode", default="ASCII", type="string", help="编码方式：[ASCII]")
    parser.add_option("-a", "--algorithm", dest="algorithm", default="HILL", type="string", help="加密算法：[HILL|DES]")
    parser.add_option("-f", "--function", dest="function", default="encrypto", type="string", help="功能：[encrypto|decrypto]")
    (options, args) = parser.parse_args()
    return options

def encrypto(options):
    decodeContent = decode_file(options.inFile, options.decode)
    decodePaddingContent = padding_content(decodeContent, "ENCODE", "ASCII", 64)
    contentBlockArray=matrix_converter(decodePaddingContent,"ENMATRIX")
    cipherBlockArray=cipher_core(contentBlockArray,generate_hill_key(64),options.function,options.algorithm,mod=128)
    cipherPaddingContent=matrix_converter(cipherBlockArray,"DEMATRIX")
    cipherText=padding_content(cipherPaddingContent,"DECODE","ASCII",64)
    encode_to_file(cipherText,options.outFile,"ASCII")
    #return cipherText

def decrypto(co,options):
    decodeContent = decode_file(options.inFile, options.decode)
    decodePaddingContent = padding_content(decodeContent, "ENCODE", "ASCII", 64)
    contentBlockArray=matrix_converter(decodePaddingContent,"ENMATRIX")
    plainBlockArray=cipher_core(contentBlockArray,generate_hill_key(64),options.function,options.algorithm,mod=128)
    plainPaddingContent=matrix_converter(plainBlockArray,"DEMATRIX")
    plainText=padding_content(plainPaddingContent,"DECODE","ASCII",64)
    return plainText

def get_algorithm(options):
    support_algorithms = ["HILL", "DES"]
    if options.algorithm in support_algorithms:
        return options.algorithm
    else:
        sys.exit("不受支持的算法，支持的算法：" + support_algorithms)


def get_function(options):
    support_functions = ["encrypto", "decrypto"]
    if options.function in support_functions:
        return options.function
    else:
        sys.exit("不受支持的功能,支持的功能" + support_functions)


# 解码文件
# 待办：支持更多解码
def decode_file(inFile, decode):
    file = open(inFile, "r")
    content = file.read()
    file.close()
    decodeContent = []
    if decode=="ASCII":
        for letter in content:
            decodeContent.append(ord(letter))
    elif decode=="":
        pass
    else:
        pass
    return decodeContent

def encode_to_file(content,outFile,encode,clear=True):
    file = open(outFile,"w",encoding="ascii")
    # 是否清空文件
    if clear:
        file.seek(0)
        file.truncate()

    encodeContent=""
    if encode=="ASCII":
        for letter in content:
            #encodeContent.join(chr(letter))
            file.write(chr(letter))
    elif encode=="":
        pass
    else:
        pass

    file.close()
    

def print_content(content):
    for letter in content:
        print(letter, end=' ')


def padding_content(content, function, code, blockSize):
    if code == "ASCII":
        paddingAscii = 0
    if function == "ENCODE":
        for i in range(int(len(content) / blockSize + 1) * blockSize - len(content)):
            content.append(paddingAscii)
    elif function == "DECODE":
        for i in range(len(content)-1, 0, -1):
            if content[i] == paddingAscii:
                del content[i]
    else:
        # 增加对功能的输入判断
        print("bUg1")
    return content

def matrix_converter(content,function,block_height=8, block_length=8):
    if function=="ENMATRIX":
        contentBlockArray = []
        for i in range(0, int(len(content) / (block_height * block_length))):
            contentBlock = []
            for j in range(0, block_height):
                contentLine = []
                for k in range(0, block_length):
                    contentLine.append(content[i * block_height * block_length + j * block_height + k])
                contentBlock.append(contentLine)
            contentBlockArray.append(contentBlock)
        return contentBlockArray
    elif function=="DEMATRIX":
        contentBlockArray=content
        content=[]
        for contentBlock in contentBlockArray:
            for contentLine in contentBlock:
                for contentItem in contentLine:
                    content.append(contentItem)
        return content
    else:
        # 增加对功能的输入判断
        print("bUg2")

def generate_hill_key(keyLen, keySapce=256):
    if np.sqrt(keyLen) != int(np.sqrt(keyLen)):
        keyLen = (int(np.sqrt(keyLen) + 1)) * (int(np.sqrt(keyLen) + 1))
        print("希尔密码密钥长度重置为" + str(keyLen))
    keyMetrix = []
    keyLine = []
    rowLen = int(np.sqrt(keyLen))
    while 1:
        for i in range(0, rowLen):
            for j in range(0, rowLen):
                keyLine.append(np.random.randint(0, 255))
            keyMetrix.append(keyLine)
            keyLine = []
        if np.linalg.det(np.array(keyMetrix)) != 0:
            # print(np.linalg.det(np.array(keyMetrix)))     # 显示行列式值
            break
        keyMetrix = []
    return keyMetrix

def cipher_core(contentArray,keyArray,function,algorithm,**arg):
    if algorithm=="HILL":
        outMetrixArray = []
        for contentBlock in contentArray:
            if function == "encrypto":
                outMetrix = hill_cipher_block(contentBlock, keyArray[1],function)
            if function == "decrypto":
                outMetrix = hill_cipher_block(contentBlock, keyArray[1],function)
            if arg["mod"] != None:
                outMetrix = np.ndarray.tolist(np.array(outMetrix) % (arg["mod"]))
            outMetrixArray.append(outMetrix)
        return outMetrixArray
    elif algorithm=="DES":
        pass
    else:
        pass

# 希尔密码 Block 处理
def hill_cipher_block(contentBlock, keyMetrix,method="encrypto"):
    outMetrix = []
    content = np.array(contentBlock)
    key = np.array(keyMetrix)
    if method == "encrypto":
        outMetrix = np.ndarray.tolist(content * key)
    if method == "decrypto":
        outMetrix = np.ndarray.tolist(content * np.linalg.inv(key))
    
    return outMetrix

if __name__ == "__main__":
    main()