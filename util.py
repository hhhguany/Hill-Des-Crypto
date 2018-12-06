import numpy as np


class BlockArray:
    contentBlockArray = [[]]

    def __init__(self, contentBlockArray=[[]]):
        self.contentBlockArray = contentBlockArray

    def block_array_is_null(self):
        return True if self.contentBlockArray == [[]] else False

    def block_array_to_content(self, block_height=8, block_length=8):
        content = []
        for contentBlock in self.contentBlockArray:
            for contentLine in contentBlock:
                for contentItem in contentLine:
                    content.append(contentItem)
        return content

    @staticmethod
    def is_block_array(object):
        return True if np.shape(np.array(object)) == 3 else False


class Content:
    content = ""

    def __init__(self, content=""):
        self.content = content

    def content_is_null(self):
        return True if self.content == None else False

    def content_to_block_array(self, block_height=8, block_length=8):
        if not (self.content_is_null()):
            contentBlockArray = []
            for i in range(0, int(len(self.content) / (block_height * block_length))):
                contentBlock = []
                for j in range(0, block_height):
                    contentLine = []
                    for k in range(0, block_length):
                        contentLine.append(self.content[i * block_height * block_length + j * block_height + k])
                    contentBlock.append(contentLine)
                contentBlockArray.append(contentBlock)
            return contentBlockArray
        else:
            print("Warning: 53415313")

    def content_add_padding(self, blockTimeSize, paddingNum=0):
        for i in range(int(len(self.content) / blockTimeSize + 1) * blockTimeSize - len(self.content)):
            self.content.append(paddingNum)

    def content_drop_padding(self, paddingNum=0):
        for i in range(len(self.content) - 1, 0, -1):
            if self.content[i] == paddingNum:
                del self.content[i]

    @staticmethod
    def string_to_line_content(string):
        lineContent=[]
        line=""
        for i in range(len(string)):
            if string[i]=="\n":
                lineContent.append(line)
                line=""
            else:
                line+=string[i]
        return lineContent

class ContentFile:
    __fileDist = ""

    def __init__(self, fileDist):
        self.__fileDist = fileDist

    def get_content(self, decode="", contentEncode="ASCII"):
        file = self.__open("r")
        content = file.read()
        file.close()
        if contentEncode == "ASCII":
            encodeContent = []
            for letter in content:
                encodeContent.append(ord(letter))
        return encodeContent

    def clear(self):
        file = open(self.__fileDist, "w")
        file.seek(0)
        file.truncate()
        file.close()

    @staticmethod
    def clear_file_content(fileDist):
        file = open(fileDist, "w")
        file.seek(0)
        file.truncate()
        file.close()

    def write_ord(self, content, encode="UTF8"):
        file = self.__open("w", encode)
        if encode == "UTF8":
            for letter in content:
                file.write(chr(letter))
        file.close()

    def __open(self, mode, coding=""):
        if coding != "":
            return open(self.__fileDist, mode, encoding=coding)
        else:
            return open(self.__fileDist, mode)

    @staticmethod
    def open_file(fileDist, mode, coding=""):
        if coding != "":
            return open(fileDist, mode, encoding=coding)
        else:
            return open(fileDist, mode)

    @staticmethod
    def write_block_to_file(fileDist, block, clear=True):
        if clear:
            ContentFile.clear_file_content(fileDist)
        file = ContentFile.open_file(fileDist, "a")
        writeContent = []
        for keyLine in block:
            for i in range(len(keyLine)):
                writeContent.append(str(keyLine[i]))
                writeContent.append(" ")
            writeContent.append("\n")
            file.writelines(writeContent)
            writeContent = []
        file.writelines("\n")
        file.close()

    @staticmethod
    def write_block_array_to_file(fileDist, blockArray):
        ContentFile.clear_file_content(fileDist)
        for block in blockArray:
            ContentFile.write_block_to_file(fileDist, block, clear=False)

    @staticmethod
    def read_file_key(fileDist,encode=""):
        file = ContentFile.open_file(fileDist,"r")
        content=file.read()
        file.close()
        content=Content.string_to_line_content(content)
        keyStringBlock=[]
        keyLine=[]
        for line in content:
            if line!="":
                line=line.split(" ")
                for i in range(len(line)):
                    if line[i]!="":
                        keyLine.append(int(line[i]))
                keyStringBlock.append(keyLine)
                keyLine=[]
        # keyBlock=Content(keyStringBlock).content_to_block_array()
        return keyStringBlock
        

    
