# -*- coding: utf-8 -*-
# 1、 密钥生成器（n维可逆方阵）
# 2、 密钥检测器（n维可逆矩阵）
# 3、 分组密码工作模式（ECB、CBC等）
# 4、 明文分组器
# contentBlockArray -> contentBlock -> contentLine -> contentList[i]
# BlockArray 为 Block 数组，在此程序中常用于存储文本分块
# Block <==> Metrix　明文块使用矩阵储存
# Line 为 Block 或 Metrix 中的一行，为 List 类型
# List(i) 为行中单独的元素

import numpy as np

# 配置项
MESSAGE_INFILE_DIST = "./message.txt"
MESSAGE_OUTFILE_DIST = ""
BLOCK_ROW = 8
BLOCK_COLUMN = 8
KEY_ROW=8
HILL_KEY=""
HILL_KEY_SPACE=256



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
def content_encode(content,encoding="ASCII",padding=False,blocksize=64,paddingAscii=0):
    out = []
    if encoding == "ASCII":
        for i in content:
            if (ord(i) >= 0 or ord(i) < 128):
                out.append(ord(i))
            else:
                print("error encoding to" + encoding)
                return []
    if padding:
        for i in range(
                int(len(content) / blocksize + 1) * blocksize - len(content)):
            out.append(paddingAscii)
    return out


# 字符串数组列表转换
# 输入文件和分割长度，输入为分割编码文件列表
def content_proc(contentList, x=8, y=8):
    contentBlockArray = []
    for i in range(0, int(len(contentList) / (x * y))):
        contentBlock = []
        for j in range(0, x):
            contentLine = []
            for k in range(0, y):
                contentLine.append(contentList[i * x * y + j * x + k])
            contentBlock.append(contentLine)
        contentBlockArray.append(contentBlock)
    return contentBlockArray


# 输出 contentBlockArray [for test]
def print_content_block_array(contentBlockArray):
    for contentBlock in contentBlockArray:
        for contentLine in contentBlock:
            print(contentLine)
        print("")

# 希尔密钥生成器
def generate_hill_key(keyLen,keySapce=256):
    if np.sqrt(keyLen)!=int(np.sqrt(keyLen)):
        keyLen = (int(np.sqrt(keyLen)+1))*(int(np.sqrt(keyLen)+1))
        print("希尔密码密钥长度重置为"+str(keyLen))
    keyMetrix=[]
    keyLine=[]
    rowLen = int(np.sqrt(keyLen))
    while 1:
        for i in range(0,rowLen):
            for j in range(0,rowLen):
                keyLine.append(np.random.random_integers(0,255))
            keyMetrix.append(keyLine)
            keyLine=[]
        if(np.linalg.det(np.array(keyMetrix))!=0):
            print(np.linalg.det(np.array(keyMetrix)))
            break;
        keyMetrix=[]        
    return keyMetrix

# 希尔密码加密
def hill_encrypto_block(contentBlock,keyMetrix):
    outMetrix = []
    content=np.array(contentBlock)
    key=np.array(key)
    outMetrix=np.ndarray.tolist(contentBlock*keyMetrix)
    return outMetrix

# def hill_
# 希尔密码解密
# def hill_decrypto(content,key):

def main():
    content = get_message_content_all(MESSAGE_INFILE_DIST)
    # content='''Hello
    # thank you
    # dsad'''

    contentList = content_encode(content, padding=True)
    contentBlockArray = content_proc(contentList)
    print_content_block_array(contentBlockArray)
    key= generate_hill_key(64)
    out = hill_encrypto(contentBlockArray,key)
    print(out)

if __name__ == "__main__":
    main()
