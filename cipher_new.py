# -*- coding: UTF-8 -*-
import sys, argprase, util, cipher
import numpy as np

## usage:
## python cipher_new.py [function] [argument]

def main():
    options = get_args()
    function_encrypt("HILL", inDist=options.inFile, outDist=options.outFile)

    input()


def get_args():
    parser = argprase.ArgumentParser(description='一个加解密小程序')
    parser.add_argument("")
    parser.add_argument("-v","--version",action="store_true",help="输出版本信息")
    parser.add_option("-i", "--infile", dest="inFile", default="message.txt", type="string", help="明文路径，默认为当前目录下 message.txt 文件")
    parser.add_option("-o", "--outfile", dest="outFile", default="output.txt", type="string", help="输出明文路径，默认输出到当前目录下 output.txt 文件")
    parser.add_option("-d", "--decode", dest="decode", default="ASCII", type="string", help="解码方式：[ASCII|UTF8]")
    parser.add_option("-e", "--encode", dest="encode", default="ASCII", type="string", help="编码方式：[ASCII|UTF8]")
    parser.add_option("-a", "--algorithm", dest="algorithm", default="HILL", type="string", help="加密算法：[HILL|DES]")
    parser.add_option("-f", "--function", dest="function", default="encrypto", type="string", help="功能：[encrypto|decrypto]")
    parser.add_option("-ghk","--generatehillkey",dest="generateHillKey",default=False)
    (options, args) = parser.parse_args()
    return options


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


def function_encrypt(algorithm, **arg):
    if algorithm == "HILL":
        contentFile = util.ContentFile(arg["inDist"])
        fileContent = contentFile.get_content()
        content = util.Content(fileContent)
        content.content_add_padding(64)
        contentBlockArray = content.content_to_block_array()

        hill = cipher.Hill(contentBlockArray)
        if arg["key"] == None:
            hillKey = hill.generate_hill_key_block(64, method="return")
            hill.set_key(hillKey)
        else:
            hill.generate_hill_key_block(64)
            
        cipherBlockArray = hill.encrypt(256)

        cipherContent = util.BlockArray(cipherBlockArray)
        content = util.Content(cipherContent.block_array_to_content())
        content.content_drop_padding()
        outFile = util.ContentFile(arg["outDist"])
        outFile.write_ord(content.content)

def function_get_hill_key()：
        

def function_decrypt(algorithm, **arg):
    if algorithm == "HILL":
        contentFile = util.ContentFile(arg["inDist"])
        fileContent = contentFile.get_content()
        content = util.Content(fileContent)
        content.content_add_padding(64)
        contentBlockArray = content.content_to_block_array()


def print_content(content):
    for letter in content:
        print(letter, end=' ')


if __name__ == "__main__":
    main()