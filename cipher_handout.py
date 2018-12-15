import numpy as np

HILL_KEY = [[21, 109, 119, 23, 88, 15, 116, 66], [22, 119, 70, 118, 111, 82, 121, 98], [79, 86, 2, 96, 90, 54, 95, 83], [22, 100, 113, 122, 92, 6, 52, 60], [1, 9, 9, 4, 112, 13, 26, 74],
            [3, 100, 92, 83, 51, 122, 102, 63], [71, 110, 92, 74, 26, 96, 92, 24], [30, 10, 85, 92, 47, 91, 114, 108]]

HILL_KEY_REVERSE = [[138, 124, 28, 104, 136, 176, 193, 182], [65, 229, 101, 214, 103, 57, 4, 224], [140, 138, 214, 71, 46, 62, 148, 184], [77, 64, 202, 44, 119, 246, 60, 86],
                    [69, 173, 41, 8, 106, 175, 255, 119], [105, 45, 131, 23, 116, 193, 29, 114], [190, 79, 82, 26, 81, 22, 187, 253], [70, 99, 51, 2, 221, 248, 152, 59]]

DES_KEY = [65, 66, 67, 68, 69, 70, 71, 72]


def get_content():
    content = input("Enter the word to encrypt:")
    return content


def string_to_ascii_list(content):
    out = []
    for letter in content:
        out.append(ord(letter))
    return out


def ascii_list_to_bin_list(asciiList, binLen=8):
    out = []
    for ascii in asciiList:
        itemBin = bin(ascii)
        for i in range(binLen + 2 - len(itemBin)):
            out.append(0)
        for b in itemBin[2:]:
            out.append(int(b))
    return out


def bin_to_string(binList, binFormatLen=8):
    out = ""
    for i in range(int(len(binList) / binFormatLen)):
        ascii = ""
        for j in range(binFormatLen):
            ascii += str(binList[i * binFormatLen + j])
        out += chr(int(ascii, 2))
    return out


def ascii_list_to_string(list):
    str = ""
    for item in list:
        str += chr(item)
    return str


def padding_content(content, blocksize=64):
    for i in range(int((len(content) - 1) / blocksize + 1) * blocksize - len(content)):
        content.append(0)
    return content


def drop_padding(content):
    for i in range(len(content)):
        if content[i] == 0:
            return content[:i]
    return content


def content_to_block_array(content):
    contentBlockArray = []
    for i in range(0, int(len(content) / 64)):
        contentBlock = []
        for j in range(0, 8):
            contentLine = []
            for k in range(0, 8):
                contentLine.append(content[i * 8 * 8 + j * 8 + k])
            contentBlock.append(contentLine)
        contentBlockArray.append(contentBlock)
    return contentBlockArray


def content_to_des_block_array(content):
    contentBlockArray = []
    for i in range(0, int(len(content) / 64)):
        contentBlock = []
        for j in range(0, 64):
            contentBlock.append(content[i * 64 + j])
        contentBlockArray.append(contentBlock)
    return contentBlockArray


def block_array_to_content(contentBlockArray, block_height=8, block_length=8):
    content = []
    for contentBlock in contentBlockArray:
        for contentLine in contentBlock:
            for contentItem in contentLine:
                content.append(contentItem)
    return content


def des_block_array_to_content(contentBlockArray):
    content = []
    for contentBlock in contentBlockArray:
        for contentLine in contentBlock:
            content.append(contentLine)
    return content


def block_to_content(contentBlock, block_height=8, block_length=8):
    content = []
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


def des_string_proc(content):
    return content_to_des_block_array(padding_content(ascii_list_to_bin_list(string_to_ascii_list(content))))


def des_ascii_list_proc(content, formatBase=8):
    return content_to_des_block_array(padding_content(ascii_list_to_bin_list(content, formatBase)))


# def des_encypt_block_array(content,keyBlock):
#     cipherBlockArray = []
#     contentBlockArray=des_content_proc(content)
#     keyBlockNum = 0
#     for contentBlock in contentBlockArray:
#         outMetrix = des_encypt_block(contentBlock, keyBlock)
#         cipherBlockArray.append(outMetrix)
#     return cipherBlockArray


def des_encypt_block_array(contentBlockArray, keyBlock, keyBlockFormatBase=8):
    cipherBlockArray = []
    subKeyArray = get_sub_key(keyBlock, keyBlockFormatBase)

    file = open("debug.txt", "a")
    file.write("\n加密子密钥：\n")
    file.writelines(str(subKeyArray))
    file.close()

    for contentBlock in contentBlockArray:
        outMetrix = des_encypt_block(contentBlock, subKeyArray, keyBlockFormatBase)
        cipherBlockArray.append(outMetrix)
    return cipherBlockArray


def des_decrypt_block_array(contentBlockArray, keyBlock, keyBlockFormatBase=8):
    cipherBlockArray = []
    subKeyArray = get_sub_key(keyBlock, keyBlockFormatBase)
    subDecryptKeyArray = subKeyArray[::-1]

    file = open("debug.txt", "a")
    file.write("\n解密子密钥：\n")
    file.writelines(str(subDecryptKeyArray))
    file.close()

    for contentBlock in contentBlockArray:
        outMetrix = des_encypt_block(contentBlock, subDecryptKeyArray, keyBlockFormatBase)
        cipherBlockArray.append(outMetrix)
    return cipherBlockArray


def list_xor(list1, list2):
    out = []
    for i in range(len(list1)):
        out.append(list1[i] ^ list2[i])
    return out


# def des_key_proc(keyBlock):
#     return ascii_list_to_bin_list(keyBlock)


def get_sub_key(keyBlock, keyBlockFormatBase=8):
    key = ascii_list_to_bin_list(keyBlock, keyBlockFormatBase)
    
    file = open("debug.txt", "a")
    file.write("\n密钥：\n")
    file.writelines(str(key))
    file.close()

    key56 = des_key_do_pc_1(key)
    keyBlock = des_key_do_shift_pc_2(key56)
    return keyBlock


def des_do_extend_permutation(content32List):
    '''扩展置换：将32位输入置换成48位输出。'''
    '''扩展置置换目标是IP置换后获得的右半部分R0，将32位输入扩展为48位(分为4位×8组)输出。'''
    E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    return [content32List[E[i] - 1] for i in range(48)]


def des_key_do_pc_1(keyList):
    '''密钥置换：不考虑每个字节的第8位，DES的密钥由64位减至56位，每个字节的第8位作为奇偶校验位。'''
    PC = [
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]
    return [keyList[PC[i] - 1] for i in range(56)]


def des_key_do_shift_pc_2(keyList):
    '''在DES的每一轮中，从56位密钥产生出不同的48位子密钥'''
    '''该处输出为所有轮次的子密钥'''
    PC = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    MOV = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    result = []
    key56=keyList
    for i in range(16):
        # 每28位为一部分，分别进行循环左移
        key0 = des_do_shift(key56[:28], MOV[i])
        key1 = des_do_shift(key56[28:], MOV[i])
        key56 = key0 + key1
        # 对56位密钥进行 PC-2 变换，将其压缩为48位
        key48 = [key56[PC[j] - 1] for j in range(48)]
        result.append(key48)
    return result


def des_do_shift(keyList, mov):
    return keyList[mov:] + keyList[:mov]


def des_do_s_box(list48):
    '''S-盒置换：将48位输入均分成长度为6的8个小组，每个小组按顺序进入相应的S盒各得到4位输出，返回合并后的32位结果。'''
    # S 盒
    S_BOX = [[
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
             [
                 [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
             ],
             [
                 [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
             ],
             [
                 [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
             ],
             [
                 [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
             ],
             [
                 [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
             ],
             [
                 [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
             ],
             [
                 [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
             ]]
    result = []
    for i in range(0, 8):
        temp = list48[i * 6:i * 6 + 6]
        row = int(str(temp[0]) + str(temp[-1]), 2)
        column = int(str(temp[1]) + str(temp[2]) + str(temp[3]) + str(temp[4]), 2)
        letter = S_BOX[i][row][column]
        result.append(letter)
    return ascii_list_to_bin_list(result, 4)


def des_do_p_box(list32):
    P_BOX = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    return [list32[P_BOX[i] - 1] for i in range(32)]


def des_do_right32(left32, right32, subKey):
    right48 = des_do_extend_permutation(right32)
    right48tmp = list_xor(right48, subKey)
    right32tmp = des_do_s_box(right48tmp)
    right32tmp = des_do_p_box(right32tmp)
    right32 = list_xor(left32, right32tmp)
    return right32


def des_encypt_block(contentBlock, subKeyArray, keyBlockFormatBase=8):
    # step1
    '''初始置换 IP'''
    text = des_do_ip(contentBlock)

    # step2
    '''16轮迭代运算'''

    # subKeyArray=get_sub_key(keyBlock,keyBlockFormatBase)
    for i in range(16):
        l,r=text[:32], text[32:]
        lNext=r
        rNext=des_do_right32(l, r, subKeyArray[i])
        text=lNext+rNext

        file = open("debug.txt", "a")
        file.write("\n第" + str(i + 1) + "轮输出：\n")
        file.writelines(str(text))
        file.close()

        # print("第"+str(i+1)+"轮输出：")
        # print(round[i])
    # step3
    '''逆初始置换IP-1'''
    text = text[32:] + text[:32]
    out = des_do_ip_inverse(text)
    return out


def des_do_ip(contentBlock):
    '''IP置换'''
    IP = [
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53,
        45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
    ]

    # content=block_to_content(contentBlock)
    return [contentBlock[IP[i] - 1] for i in range(64)]


def des_do_ip_inverse(contentBlock):
    '''IP逆置换'''
    IP_INVERSE = [
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2,
        42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
    ]
    # content=block_to_content(contentBlock)
    return [contentBlock[IP_INVERSE[i] - 1] for i in range(64)]


def hill():
    # text = content_to_block_array(padding_content(get_content()))
    message = "Typora will give you a seamless experience as both a reader and a writer. It removes the preview window, mode switcher, syntax symbols of markdown source code, and all other unnecessary distractions.."
    text = content_to_block_array(padding_content(string_to_ascii_list(message)))
    print("明文数组")
    print(text)

    # 希尔加密
    cipher = hill_encrypt_block_array(text, HILL_KEY, 256)
    cipher = drop_padding(block_array_to_content(cipher))
    print("HILL 密文：")
    # print(cipher)
    print(ascii_list_to_string(cipher))

    # 希尔解解密
    cipher = content_to_block_array(padding_content(cipher))
    plain = hill_decrypt_block_array(cipher, HILL_KEY_REVERSE, 256)
    plain = drop_padding(block_array_to_content(plain))
    print("HILL 解密文:")
    # print(plain)
    print(ascii_list_to_string(plain))

def des():
    message = "aaaaaaaa"
    # message=[15,14,15,14,15,14,15,14,15,14,15,14,15,14,15,14]
    # key=[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]z

    message = des_string_proc(message)

    file = open("debug.txt", "a")
    file.write("DES 文本：\n")
    file.writelines(str(message))
    file.write("DES 加密开始\n")
    file.close()

    # DES 加密
    cipher = des_encypt_block_array(message, DES_KEY)
    cipher = des_block_array_to_content(cipher)
    # print("DES 密文数组：")
    # print(cipher)
    print("DES 密文 ASCII：")
    print(bin_to_string(cipher))

    file = open("debug.txt", "a")
    file.write("\n\nDES 密文数组：\n")
    file.writelines(str(cipher))
    file.write("\n\nDES 解密开始\n")
    file.close()

    # DES 解密
    cipher = content_to_des_block_array(cipher)
    plain = des_decrypt_block_array(cipher, DES_KEY)
    palin = des_block_array_to_content(plain)
    # print("DES 明文数组：")
    # print(palin)
    print("DES 明文 ASCII：")
    print(bin_to_string(palin))

    file = open("debug.txt", "a")
    file.write("\n\nDES 明文数组：\n")
    file.writelines(str(palin))
    file.close()


if __name__ == "__main__":
    hill()
    des()