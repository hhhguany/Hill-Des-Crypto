# -*- coding: UTF-8 -*-
import sys, argparse, util, cipher
import numpy as np

VSRSION="Debug 1.22"
## usage:
## python cipher_new.py [function] [argument]


def main():
    options = get_args()
    function_encrypt("HILL", inDist=options.inFile, outDist=options.outFile)

    input()


def get_args():
    parser = argparse.ArgumentParser(description="一个加解密小程序")
    parser.add_argument("-i", "--infile", dest="inFile", default="message.txt", help="明文路径，默认为当前目录下 message.txt 文件")
    parser.add_argument("-o", "--outfile", dest="outFile", default="output.txt", help="输出明文路径，默认输出到当前目录下 output.txt 文件")
    parser.add_argument("-d", "--decode", dest="decode", default="ASCII", help="解码方式：[ASCII|UTF8]")
    parser.add_argument("-e", "--encode", dest="encode", default="ASCII", help="编码方式：[ASCII|UTF8]")
    parser.add_argument("-a", "--algorithm", dest="algorithm", default="HILL",  help="加密算法：[HILL|DES]")
    parser.add_argument("-f", "--function", dest="function", choices=["encrypto" ,"decrypto"],help="功能：[encrypto|decrypto]")
    parser.add_argument("--generate_hill_key", action="store_true", help="生成希尔密钥：密钥长度（需要组成方阵）")
    parser.add_argument("-v", "--version", help="VERSION %(VERSION)s, BY HE.RO")
    options = parser.parse_args()
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
        if "key" not in arg:
            hillKey = hill.generate_hill_key_block(64, method="return")
            util.ContentFile.write_key_block_to_file("key.txt", hillKey)
            hill.set_key(hillKey)
        else:
            hill.generate_hill_key_block(64)

        cipherBlockArray = hill.encrypt(256)

        cipherContent = util.BlockArray(cipherBlockArray)
        content = util.Content(cipherContent.block_array_to_content())
        content.content_drop_padding()
        outFile = util.ContentFile(arg["outDist"])
        outFile.write_ord(content.content)


def function_get_hill_key():
    pass


# def function_decrypt(algorithm, **arg):
#     if algorithm == "HILL":
#         contentFile = util.ContentFile(arg["inDist"])
#         fileContent = contentFile.get_content()
#         content = util.Content(fileContent)
#         content.content_add_padding(64)
#         contentBlockArray = content.content_to_block_array()


def print_content(content):
    for letter in content:
        print(letter, end=' ')


if __name__ == "__main__":
    main()