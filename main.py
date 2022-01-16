import binascii,copy
import numpy as np
from PIL import Image

SAVEPATH = ".\\output\\"
FONTLIB = "HZK16H"
LIB = ".\\lib\\"
L = ['，','。','（','）','、','“','”']
N = ['１','２','３','４','５','６','７','８','９','０']
def IS_CHINESE(ch):
    if '\u4e00' <= ch <= '\u9fff' or ch in L or ch in N:
        return True
    return False
    
def CHA2HZK16(word): 
    KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
    rect_list = [] * 16
    for i in range(16):
        rect_list.append([] * 16)
    text = word
    if not IS_CHINESE(word):
        return np.zeros((16,16),dtype = int)
    gb2312 = text.encode('gb2312')
    hex_str = binascii.b2a_hex(gb2312)
    result = str(hex_str, encoding='utf-8')
    area = eval('0x' + result[:2]) - 0xA0
    index = eval('0x' + result[2:]) - 0xA0
    offset = (94 * (area-1) + (index-1)) * 32
    font_rect = None
    with open(".\\font_libs\\HZK\\16\\"+FONTLIB, "rb") as f:
        f.seek(offset)
        font_rect = f.read(32)
    for k in range(len(font_rect) // 2):
        row_list = rect_list[k]
        for j in range(2):
            for i in range(8):
                asc = font_rect[k * 2 + j]
                flag = asc & KEYS[i]
                row_list.append(flag)
    if FONTLIB == 'HZK16':
        rect_list = np.array(rect_list).T
    res = copy.deepcopy(rect_list)
    for i in range(16):
        for j in range(16):
            if res[i][j]!=0:
                res[i][j]='1'
    return res

def LETTER216(lt):
    KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
    rect_list = [] * 16
    for i in range(16):
        rect_list.append([] * 16)
    offset = ord(lt)
    with open(".\\font_libs\\ASC\\ASC16_8", "rb") as f:
        f.seek((offset-32)*16)
        font_rect = f.read(16)
    for i in range(16):
        row_list = rect_list[i]
        for j in range(8):
            index = j*16+i
            flag = font_rect[index//8] & KEYS[index%8]
            row_list.append(flag)
    for i in range(16):
        for j in range(8):
            if rect_list[i][j]>0:
                rect_list[i][j]=1
    return np.array(rect_list)

def DrawCharacter(ch):
    src = CHA2HZK16(ch)
    output = np.zeros((16,16,3),dtype='uint8')
    WHITE = [255,255,255]
    BLACK = [0,0,0]
    for i in range(0,16):
        for j in range(0,16):
            if src[i][j] == 0:
                output[i][j] = BLACK
            else:
                output[i][j] = WHITE
    return output

def DrawLetter(ch):
    src = LETTER216(ch)
    output = np.zeros((16,8,3),dtype='uint8')
    WHITE = [255,255,255]
    BLACK = [0,0,0]
    for i in range(0,16):
        for j in range(0,8):
            if src[i][j] == 0:
                output[i][j] = BLACK
            else:
                output[i][j] = WHITE
    return output

def drawOnePic(L1,L2,savename,savepath=".\\output\\",snow = 1,kt = 1):
    ept = Image.open(LIB+'empty.bmp')
    output = np.array(ept)
    L1Len = 0
    L2Len = 0
    if kt:
        L1 = "空调 "+L1
    if snow :
        L1Len += 16
        SN = np.array(Image.open(LIB+'snow.png').convert("RGB"))
    offset = 0
    width = 0

    for chs in L1:
        if IS_CHINESE(chs):
            L1Len+=16
        else:
            L1Len+=8 
    for chs in L2:
        if IS_CHINESE(chs):
            L2Len+=16
        else:
            L2Len+=8

    offset = (128-L1Len)//2
    if snow:
        for i in range(16):
            for j in range(offset,offset+16):
                output[i][j] = SN[i][j-offset]
        offset += 16

    for c in L1:
        if IS_CHINESE(c):
            mid = DrawCharacter(c)
            width = 16
        else:
            mid = DrawLetter(c)
            width = 8
        for i in range(16):
            for j in range(offset,offset+width):
                output[i][j] = mid[i][j-offset]
        offset+=width

    offset = 0
    for c in L2:
        if IS_CHINESE(c):
            mid = DrawCharacter(c)
            width = 16
        else:
            mid = DrawLetter(c)
            width = 8
        for i in range(16,32):
            for j in range(offset,offset+width):
                output[i][j] = mid[i-16][j-offset]
        offset+=width
    O = Image.fromarray(output)
    O.save(savepath+savename+'.png')

def main(filename,savepath = '.\\output\\',snow = 1,kt = 1,type=0):
    with open(filename, "r",encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if lines[i][-1] == '\n':
            lines[i] = lines[i][:-1]
    for L in lines:
        name,route,dest = L.split('\t')
        if type == 0:
            L1 = route
            L2 = route+'->'+dest
        elif type == 1:
            L1 = route
            L2 = dest
        drawOnePic(L1,L2,name,savepath=savepath,snow=snow,kt=kt)
main('.\src.txt',snow=0,kt=0,type = 1)
'''
snow 雪花标志 1 为自动在头显加入雪花标志
kt "空调" 字样  1 为自动加入空调字样
type : 0表示只需要在第三列写入终点，自动生成：线路名->终点站侧显
       1表示自由定义第三列
'''
