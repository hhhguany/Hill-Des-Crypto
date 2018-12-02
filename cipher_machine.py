# -*- coding: utf-8 -*-
# 1、 密钥生成器（n维可逆方阵）
# 2、 密钥检测器（n维可逆矩阵）
# 3、 分组密码工作模式（ECB、CBC等）
# 4、 明文分组器
# contentBlockArray -> contentBlock -> contentLine -> contentList[i]
# BlockArray 为 Block 数组，在此程序中常用于存储文本分块,[[[1,2],[3,4]],[[5,6],[7,8]]
# Block <==> Metrix　明文块使用矩阵储存,[[1,2][3,4]]
# Line 为 Block 或 Metrix 中的一行，为 List 类型,[1,2]
# List(i) 为行中单独的元素,[1]

import numpy as np

# 配置项
MESSAGE_INFILE_DIST = "./message.txt"
MESSAGE_OUTFILE_DIST = ""
BLOCK_ROW = 8
BLOCK_COLUMN = 8
KEY_ROW = 8
HILL_KEY = ""
HILL_KEY_SPACE = 256


# 获取文件全部内容
# 输入：文件路径 fileDist
# 输出：文件内容；默认编码字符串
def get_message_content_all(fileDist):
    infile = open(fileDist, "r")
    content = infile.read()
    infile.close()
    return content

# 字符串格式化编码
# 输入： 内容 content | 编码格式 encoding | padding 是否填充 | blocksize 填充分段大小 | 填充内容
# 输出：格式化编码字符串
def content_encode(content, encoding="None",decoding="None", padding=False, blocksize=64, paddingAscii=0):
    out = []
    if encoding == "ASCII":
        for i in content:
            if ord(i) >= 0 or ord(i) < 128:
                out.append(ord(i))
            else:
                print("error encoding to" + encoding)
                return []
    if padding:
        for i in range(int(len(content) / blocksize + 1) * blocksize - len(content)):
            out.append(paddingAscii)
    return out

def content_padding(content,method="add",paddingAscii="0",paddingBlockSize=64):
    if method=="add":
        for i in range(int(len(content) / paddingBlockSize + 1) * paddingBlockSize - len(content)):
            content.append(paddingAscii)
    elif method=="drop":
        for i in range(len(content),0,-1):
            if content(i)==paddingAscii:
                del content[i]
    else:
        print("Warning : content_padding() : no use")
    return content

# 字符串数组列表转换
# 输入文件和分割长度，输入为分割编码文件列表
def content_to_block_array(content, block_height=8, block_length=8):
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

def block_array_to_content(contentBlockArray):
    content=[]
    for contentBlock in contentBlockArray:
        for contentLine in contentBlock:
            for contentItem in contentLine:
                content.append(contentItem)
    return content

# BlockArray 编解码
def block_array_coding(contentBlockArray,method="encode",coding="ASCII"):
    outContentBlockArray=[]
    for contentBlock in contentBlockArray:
        outContentBlock=[]
        for contentLine in contentBlock:
            outContentLine=[]
            for content in contentLine:
                if coding=="ASCII":
                    if method=="encode":
                        outContentLine.append(ord(content))
                    if method=="decode":
                        outContentLine.append(ascii(content))
            outContentBlock.append(outContentLine)
        outContentBlockArray.append(outContentBlock)
    return outContentBlockArray

# 打印 contentBlockArray [for test]
def print_content_block_array(contentBlockArray):
    for contentBlock in contentBlockArray:
        for contentLine in contentBlock:
            print(contentLine)
        print("")

# 希尔密钥 Block 生成器
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

# 希尔密码 Block 处理
def hill_crypto_block(contentBlock, keyMetrix,method="encrypto"):
    outMetrix = []
    content = np.array(contentBlock)
    key = np.array(keyMetrix)
    if method == "encrypto":
        outMetrix = np.ndarray.tolist(content * key)
    if method == "decrypto":
        outMetrix = np.ndarray.tolist(content * np.linalg.inv(key))
    
    return outMetrix

# 希尔密码 Blocke Array 处理
def hill_crypto(contentBlockArray, keyMetrixArray, method="encrypto", **arg):
    outMetrixArray = []
    for contentBlock in contentBlockArray:
        if method == "encrypto":
            outMetrix = hill_crypto_block(contentBlock, keyMetrixArray[1],method)
        if method == "decrypto":
            outMetrix = hill_crypto_block(contentBlock, keyMetrixArray[1],method)
        if arg["mod"] != None:
            outMetrix = np.ndarray.tolist(np.array(outMetrix) % (arg["mod"]))
        outMetrixArray.append(outMetrix)
    return outMetrixArray

def get_plain_text(fileDist):
    plainText = get_message_content_all(fileDist)
    asciiContent=content_encode(plainText,"ASCII",padding=True)
    asciiContentBlockArray=content_to_block_array(asciiContent,8,8)
    return asciiContentBlockArray

def get_cipher_text(outContentBlockArray):
    outContentBlockArray=block_array_coding(outContentBlockArray,"decode")
    outContent=block_array_to_content(outContentBlockArray)
    return outContent

def main():
    plainText = get_plain_text(MESSAGE_INFILE_DIST)
    keyMetrix = generate_hill_key(64)
    cipherText = get_cipher_text(hill_crypto(plainText,keyMetrix,"encrypto",mod=128))
    print(cipherText)

if __name__ == "__main__":    
    main()
