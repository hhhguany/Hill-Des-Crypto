import numpy as np

class BlockArray:
    contentBlockArray = [[]]
    def __init__(self, contentBlockArray=[[]]):
        self.contentBlockArray = contentBlockArray

    def content_block_array_is_null(self):
        return True if self.contentBlockArray == None else False
    
    def block_array_to_content(self,block_height=8, block_length=8):
        content = []
        for contentBlock in self.contentBlockArray:
            for contentLine in contentBlock:
                for contentItem in contentLine:
                    content.append(contentItem)
        return content

    def is_block_array(object):
        return True if np.shape(np.array(object))==3 else False
            


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
        for i in range(int(len(self.content) / blockSize + 1) * blockSize - len(self.content)):
            self.content.append(paddingNum)

    def content_drop_padding(self, paddingNum=0):
        for i in range(len(self.content) - 1, 0, -1):
            if self.content[i] == paddingNum:
                del self.content[i]


class ContentFile:
    __fileDist = ""

    def __init__(self, fileDist):
        self.__fileDist = fileDist

    def get_content(self, decode=""):
        file = self.__open_file("r")
        content = file.read()
        file.close()
        return content

    def clear_content(self):
        file = self.__open_file("w")
        file.seek(0)
        file.truncate()
        file.close()

    def write_ord(self, content, encode="UTF8"):
        file = self.__open_file("w", "UTF8")
        for letter in content:
            file.write(chr(letter))
        file.close()

    def __open_file(self, mode, coding=""):
        if coding != None:
            return open(self.__fileDist, mode, encoding=coding)
        else:
            return open(self.__fileDist, mode)


if __name__ == "__main__":
    a = ContentProcess()
    a.content = "ffadfdafadfdafda"
    a.content_to_block_array(2, 4)
    for i in a.contentBlockArray:
        print(i)
