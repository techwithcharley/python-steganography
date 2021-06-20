from PIL import Image
import time
import os

class Stego():
    def ImageAnalyser(self,carrier):
        self.userin = Image.open(carrier)
        self.RGB_userin = self.userin.convert('RGB')
        self.width, self.height = self.userin.size
        self.new_array = []

        for h in range(self.height):
            for w in range((self.width)):
                self.r,self.g,self.b = self.RGB_userin.getpixel((w,h))
                self.ip = (self.r,self.g,self.b)
                self.new_array.append(self.ip)
        return self.new_array

    def ArrayConverter(self,RGB_array):
        self.bin_array = []
        for item in range(len(RGB_array)):
            self.colour = RGB_array[item]
            self.r,self.g,self.b = self.colour[0],self.colour[1],self.colour[2]
            self.r_bin,self.g_bin,self.b_bin = bin(self.r),bin(self.g),bin(self.b)
            self.r_bin = self.r_bin.replace('0b', '')
            self.g_bin = self.g_bin.replace('0b', '')
            self.b_bin = self.b_bin.replace('0b', '')
            self.r_bin = self.r_bin.zfill(8)
            self.g_bin = self.g_bin.zfill(8)
            self.b_bin = self.b_bin.zfill(8)
            self.bin_array.append(self.r_bin)
            self.bin_array.append(self.g_bin)
            self.bin_array.append(self.b_bin)
        return self.bin_array

class Encode(Stego):
    def __init__(self,cover,hide,outfile):
        self.cover = cover
        self.hide = hide
        self.outfile = outfile
        
        def ImageEncoder(self,cover,hide,outfile):
            self.cover_size = Image.open(self.cover)
            self.cover_size = self.cover_size.size
            self.hide_size = Image.open(self.hide)
            self.hide_size = self.hide_size.size
            self.mult_Wid = self.cover_size[0] / self.hide_size[0]
            self.mult_Hei = self.cover_size[1] / self.hide_size[1]
            self.size = os.path.getsize(self.cover)
            self.max_size = os.path.getsize("P:\Programs\Fork\Steganography\Semester 2 Project - Steganography\Images\cover-2360x2360.bmp")

            if self.mult_Wid == 2 and self.mult_Hei == 2:

                if self.size < self.max_size:
            
                    self.cover_RGB = self.ImageAnalyser(self.cover)
                    self.hide_RGB = self.ImageAnalyser(self.hide)
                    self.cover_bin = self.ArrayConverter(self.cover_RGB)
                    self.hide_bin = self.ArrayConverter(self.hide_RGB)
                    self.make = Image.new('RGB', self.cover_size, 'white')
                    self.binary_array,self.hide_array,self.op_array,self.RGB = [],[],[],[]
                    self.timer = 0
                    self.count = 3

                    for item in range(len(self.hide_bin)):
                        self.hide_bit = self.hide_bin[item]
                        self.hide_bit_1 = self.hide_bit[0:2]
                        self.hide_bit_2 = self.hide_bit[2:4]
                        self.hide_bit_3 = self.hide_bit[4:6]
                        self.hide_bit_4 = self.hide_bit[6:8]
                        self.hide_array.append(self.hide_bit_1)
                        self.hide_array.append(self.hide_bit_2)
                        self.hide_array.append(self.hide_bit_3)
                        self.hide_array.append(self.hide_bit_4)
            
                    for val in range(len(self.cover_bin)):
                        self.cover_bit = str(self.cover_bin[val])
                        self.cover_bit_1 = self.cover_bit[0:6]
                        self.binary_val = self.cover_bit_1 + self.hide_array[self.timer]
                        self.binary_array.append(self.binary_val)
                        self.timer += 1

                    for i in range(0,len(self.binary_array)-2,3):
                        self.binary_1 = self.binary_array[i:self.count]
                        self.RGB_1 = int(str(self.binary_1[0]), 2)
                        self.RGB_2 = int(str(self.binary_1[1]), 2)
                        self.RGB_3 = int(str(self.binary_1[2]), 2)
                        self.Tup = tuple([self.RGB_1,self.RGB_2,self.RGB_3])
                        self.op_array.append(self.Tup)
                        self.count += 3

                    self.im = self.make.putdata(self.op_array)
                    self.im = self.make.save(outfile)

                else:
                    print("File size too large")

            else:
                print("Error: Cover image size must be 2x image to hide")
            
        output = ImageEncoder(self,cover,hide,outfile)

class Decode(Stego):
    def __init__(self,hide,Object,output):
        self.object = Object
        self.output = output
        self.object_open = Image.open(Object)
        self.object_size = self.object_open.size
        self.hidden_size = ((int(self.object_size[0] / 2)),(int(self.object_size[1] / 2)))
        self.object_RGB = self.ImageAnalyser(self.object)
        self.object_bin = self.ArrayConverter(self.object_RGB)

        def ImageDecoder(self,Object,output):
            self.make = Image.new('RGB', self.hidden_size, 'white')
            self.hidden_seq = []
            self.hidden_array = []
            self.time = 12

            for j in range(len(self.object_bin)):
                self.object_val = self.object_bin[j]
                self.val = self.object_val[6:8]
                self.hidden_seq.append(self.val)

            for k in range(0,len(self.hidden_seq),12):
                self.bit = self.hidden_seq[k:self.time]
                self.bit_RGB_1 = self.bit[0]+self.bit[1]+self.bit[2]+self.bit[3]
                self.bit_RGB_2 = self.bit[4]+self.bit[5]+self.bit[6]+self.bit[7]
                self.bit_RGB_3 = self.bit[8]+self.bit[9]+self.bit[10]+self.bit[11]
                self.bit_RGB_1 = int(self.bit_RGB_1, 2)
                self.bit_RGB_2 = int(self.bit_RGB_2, 2)
                self.bit_RGB_3 = int(self.bit_RGB_3, 2)
                self.tuple = tuple([self.bit_RGB_1,self.bit_RGB_2,self.bit_RGB_3])
                self.hidden_array.append(self.tuple)
                self.time +=12

            self.im = self.make.putdata(self.hidden_array)
            self.im = self.make.save("retrieved.bmp")

        decoded = ImageDecoder(self,Object,output)

#Im_Encoded = Encode('cover.bmp','hide.bmp','object.bmp')
#Im_Decoded = Decode('object.bmp','retrieved.bmp')

Im_Encoded = Encode("P:\Programs\Fork\Steganography\Semester 2 Project - Steganography\Images\cover.bmp","P:\Programs\Fork\Steganography\Semester 2 Project - Steganography\Images\hide.bmp","P:\Programs\Fork\Steganography\Semester 2 Project - Steganography\Images\object.bmp")
Im_Decoded = Decode("P:\Programs\Fork\Steganography\Semester 2 Project - Steganography\Images\hide.bmp","P:\Programs\Fork\Steganography\Semester 2 Project - Steganography\Images\object.bmp","P:\Programs\Fork\Steganography\Semester 2 Project - Steganography\Images\retrieved.bmp")
