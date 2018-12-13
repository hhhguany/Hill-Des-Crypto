import numpy as np

# yapf: disable
HILL_KEY = [[21, 109, 119, 23, 88, 15, 116, 66], [22, 119, 70, 118, 111, 82, 121, 98], [79, 86, 2, 96, 90, 54, 95, 83], [22, 100, 113, 122, 92, 6, 52, 60], [1, 9, 9, 4, 112, 13, 26, 74],
            [3, 100, 92, 83, 51, 122, 102, 63], [71, 110, 92, 74, 26, 96, 92, 24], [30, 10, 85, 92, 47, 91, 114, 108]]

HILL_KEY_REVERSE = [[138, 124, 28, 104, 136, 176, 193, 182], [65, 229, 101, 214, 103, 57, 4, 224], [140, 138, 214, 71, 46, 62, 148, 184], [77, 64, 202, 44, 119, 246, 60, 86],
                    [69, 173, 41, 8, 106, 175, 255, 119], [105, 45, 131, 23, 116, 193, 29, 114], [190, 79, 82, 26, 81, 22, 187, 253], [70, 99, 51, 2, 221, 248, 152, 59]]

IP = [[58, 50, 42, 34, 26, 18, 10, 2],
    [60, 52, 44, 36, 28, 20, 12, 4],
    [62, 54, 46, 38, 30, 22, 14, 6],
    [64, 56, 48, 40, 32, 24, 16, 8],
    [57, 49, 41, 33, 25, 17, 9, 1],
    [59, 51, 43, 35, 27, 19, 11, 3],
    [61, 53, 45, 37, 29, 21, 13, 5],
    [63, 55, 47, 39, 31, 23, 15, 7]]
# P 盒逆IP_I
NV = []

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

def get_content():
    content=input("Enter the word to encrypt:")
    out=[]
    for letter in content:
        out.append(ord(letter))
    return out
    

def ascii_list_to_string(list):
    str=""
    for item in list:
        str+=chr(item)
    return str

def padding_content(content):
    for i in range(int(len(content) / 64 + 1) * 64 - len(content)):
        content.append(0)
    return content

def drop_padding(content):
    for i in range(len(content)):
        if content[i]==0:
            return content[:i]
    return content

def content_to_block_array(content):
    contentBlockArray = []
    for i in range(0, int(len(content)/64)):
        contentBlock = []
        for j in range(0, 8):
            contentLine = []
            for k in range(0, 8):
                contentLine.append(content[i * 8 * 8 + j * 8 + k])
            contentBlock.append(contentLine)
        contentBlockArray.append(contentBlock)
    return contentBlockArray

def block_array_to_content(contentBlockArray, block_height=8, block_length=8):
    content = []
    for contentBlock in contentBlockArray:
        for contentLine in contentBlock:
            for contentItem in contentLine:
                content.append(contentItem)
    return content

def hill_encrypt_block_array(contentBlockArray, keyBlock, field):
    cipherBlockArray = []
    keyBlockNum = 0
    for contentBlock in contentBlockArray:
        outMetrix = hill_encrypt_block(contentBlock, keyBlock, field)
        cipherBlockArray.append(outMetrix)
    return cipherBlockArray


def hill_decrypt_block_array(contentBlockArray, keyBlock, field):
    plainBlockArray = []
    for contentBlock in contentBlockArray:
        outMetrix = hill_decrypt_block(contentBlock, keyBlock, field)
        plainBlockArray.append(outMetrix)
    return plainBlockArray

def hill_encrypt_block(contentBlock, keyBlock, field):
    cipherBlock = []
    contentArray = np.array(contentBlock)
    keyArray = np.array(keyBlock)
    cipherBlock = np.ndarray.tolist(np.dot(contentArray, keyArray) % field)
    return cipherBlock

def hill_decrypt_block(contentBlock, keyBlock, field):
    plainBlock = []
    contentArray = np.array(contentBlock)
    keyArray = np.array(keyBlock)
    plainBlock = np.ndarray.tolist(np.dot(contentArray, keyArray) % field)
    return plainBlock

def des_encypt_block_array(contentBlockArray,keyBlock):
    cipherBlockArray = []
    keyBlockNum = 0
    for contentBlock in contentBlockArray:
        outMetrix = hill_encrypt_block(contentBlock, keyBlock, field)
        cipherBlockArray.append(outMetrix)
    return cipherBlockArray

def des_encypt_block(contentBlock,keyBlock):
    step1=des_do_ip(contentBlock)
    return step1

def des_do_ip(contentBlock):
    content=block_array_to_content(contentBlock)
    ipList=block_array_to_content(IP)
    out=content
    for i in range(len(content)):
        out[i]=content[ipList[i]]
    return out


if __name__ == "__main__":
    text = content_to_block_array(padding_content(get_content()))
    # text="dasfshjfahjfhlaskfhjlhahjdkasfhlasdkfjlshk"
    # text = content_to_block_array(padding_content(string_to_list(text)))
    print("明文：\n")
    print(text)

    # 希尔加密
    cipher=hill_encrypt_block_array(text,HILL_KEY,256)
    cipher=drop_padding(block_array_to_content(cipher))
    print("密文：")
    # print(cipher)
    print(ascii_list_to_string(cipher))

    # 希尔解解密
    cipher=content_to_block_array(padding_content(cipher))
    plain=hill_decrypt_block_array(cipher,HILL_KEY_REVERSE,256)
    plain=drop_padding(block_array_to_content(plain))
    print("解密文:")
    # print(plain)
    print(ascii_list_to_string(plain))

