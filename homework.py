# -*- coding: UTF-8 -*-

'''
作业：
假设DES 算法的明文输入M=FEFEFEFEFEFEFEFE，密钥K=55555555555555
（均为16 进制表示，密钥没有校验位），求第一轮的输出。
'''
def to_bin(hex,base=16,formatLen=4):
    '''输入每一个base进制字符被转换成formatLen位二进制'''
    out,_bin=[],""
    for item in hex:
        _bin=bin(int(item,base))[2:] if base!=10 else bin(item)[2:]
        tmp=[0 for i in range(formatLen-len(_bin))]+[int(i) for i in list(_bin)]
        out+=tmp
    return out

def bin_to_hex(bin,formatLen=4):
    tmp1=[bin[i*formatLen:(i+1)*formatLen] for i in range(int(len(bin)/formatLen))]
    tmp3=[]
    for item in tmp1:
        tmp2=""
        for iitem in item:
            tmp2+=str(iitem)
        tmp3.append(hex(int(tmp2,2))[2:])
    return tmp3


def special_key_proc(bin56):
    '''专用于此题的密钥处理方法，即56位不带校验位的密钥读入，自动生成为64位密钥'''
    bin64=[]
    for i in range(8):
        bin64+=bin56[i*7:i*7+7]+[0]
    return bin64

def des_do_ip(contentBlock):
    '''IP置换'''
    IP = [
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53,
        45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
    ]
    return [contentBlock[IP[i] - 1] for i in range(64)]

def des_key_do_pc_1(key64):
    '''密钥初始置换：不考虑每个字节的第8位，DES的密钥由64位减至56位，每个字节的第8位作为奇偶校验位。'''
    PC = [
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]
    return [key64[PC[i] - 1] for i in range(56)]

def des_key_do_pc_2(key56):
    PC = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    return [key56[PC[j] - 1] for j in range(48)]

def des_do_shift(keyList, mov):
    return keyList[mov:] + keyList[:mov]

def list_xor(list1, list2):
    return [list1[i] ^ list2[i] for i in range(len(list1))]


def des_do_extend_permutation(content32List):
    '''扩展置换：将32位输入置换成48位输出。'''
    '''扩展置置换目标是IP置换后获得的右半部分R0，将32位输入扩展为48位(分为4位×8组)输出。'''
    E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    return [content32List[E[i] - 1] for i in range(48)]

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
    return to_bin(result,10)

def des_do_p_box(list32):
    P_BOX = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    return [list32[P_BOX[i] - 1] for i in range(32)]

def mian():
    M="FEFEFEFEFEFEFEFE"
    K="55555555555555"

    message=to_bin(M)
    key=special_key_proc(to_bin(K))
    print("二进制：")
    print(message)
    print("加密密钥二进制：")
    print(key)

    messageTmp1=des_do_ip(message)
    print("加密消息经过IP置换后：")
    print(messageTmp1)

    keyTmp1=des_key_do_pc_1(key)
    print("加密密钥经过PC-1置换后：")
    print(keyTmp1)

    key0 = des_do_shift(keyTmp1[:28], 1)
    key1 = des_do_shift(keyTmp1[28:], 1)
    keyTmp2=key0+key1
    print("加密密钥位移变换后：")
    print(keyTmp2)

    keyTmp3=des_key_do_pc_2(keyTmp2)
    print("加密密钥经过PC-2置换后，得到第一轮子密钥：")
    print(keyTmp3)

    left32,right32=messageTmp1[:32], messageTmp1[32:]
    rightNext32Tmp1=des_do_extend_permutation(right32)
    print("IP置换后的右半部分扩展置换结果：")
    print(rightNext32Tmp1)

    rightNext32Tmp2=list_xor(rightNext32Tmp1,keyTmp3)
    print("第一轮密钥异或结果：")
    print(rightNext32Tmp2)

    rightNext32Tmp3=des_do_s_box(rightNext32Tmp2)
    print("S-盒结果：")
    print(rightNext32Tmp3)

    rightNext32Tmp4=des_do_p_box(rightNext32Tmp3)
    print("P-盒结果：")
    print(rightNext32Tmp4)

    rightNext32=list_xor(rightNext32Tmp4,left32)
    print("下一轮右半部分：")
    print(rightNext32)

    nextRound=right32+rightNext32
    print("第一轮二进制输出：")
    print(nextRound)

    hex=bin_to_hex(nextRound)
    print("第一轮hex输出：")
    print(hex)




if __name__ == "__main__":
    mian()
