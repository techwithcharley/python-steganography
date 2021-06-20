#Import all required libraries
from PIL import Image
import time
import os

#Define a new class called 'Stego'
class Stego():
    #Define a new function called 'ImageAnalyser'
    def ImageAnalyser(self,carrier):
        #Open the image that is passed into the function
        self.userin = Image.open(carrier)
        #Convert the image into RGB
        self.RGB_userin = self.userin.convert('RGB')
        #Store the dimensions of the image in two variables
        self.width, self.height = self.userin.size
        #Create a new, empty array
        self.new_array = []

        #Create an iteration for each value of the height
        for h in range(self.height):
            #Create an iteration for each value of the width
            for w in range((self.width)):
                #Store the R, G, and B values of each pixel in three variables
                self.r,self.g,self.b = self.RGB_userin.getpixel((w,h))
                #Add the variables to a list
                self.ip = (self.r,self.g,self.b)
                #Append the list to 'new_array'
                self.new_array.append(self.ip)
        #Return the 'new_array' from the function
        return self.new_array

    #Define a new function called 'ArrayConverter'
    def ArrayConverter(self,RGB_array):
        #Create a new, empty array
        self.bin_array = []
        #Create an iteration for each value in the length of 'RGB_array'
        for item in range(len(RGB_array)):
            #Store each pixel's data in a variable
            self.colour = RGB_array[item]
            #Store the R, G, and B values in separate variables
            self.r,self.g,self.b = self.colour[0],self.colour[1],self.colour[2]
            #Cast the R, G, and B values to binary
            self.r_bin,self.g_bin,self.b_bin = bin(self.r),bin(self.g),bin(self.b)
            #Remove the signing bits at the beginning of the sequence
            self.r_bin = self.r_bin.replace('0b', '')
            self.g_bin = self.g_bin.replace('0b', '')
            self.b_bin = self.b_bin.replace('0b', '')
            #Ensure that the binary sequence is 8 bits in length
            self.r_bin = self.r_bin.zfill(8)
            self.g_bin = self.g_bin.zfill(8)
            self.b_bin = self.b_bin.zfill(8)
            #Append the binary sequences to 'bin_array'
            self.bin_array.append(self.r_bin)
            self.bin_array.append(self.g_bin)
            self.bin_array.append(self.b_bin)
        #Return 'bin_array' from the function
        return self.bin_array

#Define a new class called 'Encode'
class Encode(Stego):
    #Define an init function within 'Encode'
    def __init__(self,cover,hide,outfile):
        #Store the user inputs within variables
        self.cover = cover
        self.hide = hide
        self.outfile = outfile

        #Define a new function called 'ImageEncoder'
        def ImageEncoder(self,cover,hide,outfile):
            #Open the cover image
            self.cover_size = Image.open(self.cover)
            #Get the dimensions of the cover image
            self.cover_size = self.cover_size.size
            #Open the image to hide
            self.hide_size = Image.open(self.hide)
            #Get the dimensions of the image to hide
            self.hide_size = self.hide_size.size
            #Calculate the relationship between the image widths
            self.mult_Wid = self.cover_size[0] / self.hide_size[0]
            #Calculate the relationship between the image heights
            self.mult_Hei = self.cover_size[1] / self.hide_size[1]
            #Get the file size of the cover image
            self.size = os.path.getsize(self.cover)
            #Get the file size of the maximum image size
            self.max_size = os.path.getsize('cover-2360x2360.bmp')

            #Ensure that the cover image and image to hide are the same aspect ratio
            if self.mult_Wid == 2 and self.mult_Hei == 2:

                #Ensure that the size of the cover image is less than the maximum
                if self.size < self.max_size:

                    #Create instances of the 'ImageAnalyser' function
                    self.cover_RGB = self.ImageAnalyser(self.cover)
                    self.hide_RGB = self.ImageAnalyser(self.hide)
                    #Create instances of the 'ArrayConverter' function
                    self.cover_bin = self.ArrayConverter(self.cover_RGB)
                    self.hide_bin = self.ArrayConverter(self.hide_RGB)
                    #Create a new, blank image
                    self.make = Image.new('RGB', self.cover_size, 'white')
                    #Create four new, empty arrays
                    self.binary_array,self.hide_array,self.op_array,self.RGB = [],[],[],[]
                    #Create two variables for timing
                    self.timer = 0
                    self.count = 3

                    #Create an iteration for each value in the length of 'hide_bin'
                    for item in range(len(self.hide_bin)):
                        #Store each value in a variable
                        self.hide_bit = self.hide_bin[item]
                        #Separate each value into four 2-bit sequences
                        self.hide_bit_1 = self.hide_bit[0:2]
                        self.hide_bit_2 = self.hide_bit[2:4]
                        self.hide_bit_3 = self.hide_bit[4:6]
                        self.hide_bit_4 = self.hide_bit[6:8]
                        #Append each 2-bit sequence to 'hide_array'
                        self.hide_array.append(self.hide_bit_1)
                        self.hide_array.append(self.hide_bit_2)
                        self.hide_array.append(self.hide_bit_3)
                        self.hide_array.append(self.hide_bit_4)

                    #Create an iteration for each value in the length of 'cover_bin'
                    for val in range(len(self.cover_bin)):
                        #Cast each value to a string
                        self.cover_bit = str(self.cover_bin[val])
                        #Select the first six bits of the value
                        self.cover_bit_1 = self.cover_bit[0:6]
                        #Add one of the 2-bit sequences from 'hide_array' to the 6-bit sequence
                        self.binary_val = self.cover_bit_1 + self.hide_array[self.timer]
                        #Append the new value to 'binary_array'
                        self.binary_array.append(self.binary_val)
                        #Increase timer by 1
                        self.timer += 1

                    #Create an iteration for each value in the length of 'binary_array'
                    for i in range(0,len(self.binary_array)-2,3):
                        #Select three values from 'binary_array'
                        self.binary_1 = self.binary_array[i:self.count]
                        #Cast all three values to decimal
                        self.RGB_1 = int(str(self.binary_1[0]), 2)
                        self.RGB_2 = int(str(self.binary_1[1]), 2)
                        self.RGB_3 = int(str(self.binary_1[2]), 2)
                        #Cast a list of the three values to a tuple
                        self.Tup = tuple([self.RGB_1,self.RGB_2,self.RGB_3])
                        #Append the tuple to 'op_array'
                        self.op_array.append(self.Tup)
                        #Increase count by 3
                        self.count += 3

                    #Add the data from 'op_array' to the blank image
                    self.im = self.make.putdata(self.op_array)
                    #Save the image with the new data added
                    self.im = self.make.save(outfile)

                #Return an error if the file size of the cover image is too large
                else:
                    print("File size too large")

            #Return an error if the aspect ratio of the images is not identical
            else:
                print("Error: Cover image size must be 2x image to hide")

        #Create an instance of the 'ImageEncoder' function
        output = ImageEncoder(self,cover,hide,outfile)

#Define a new class called 'Decode'
class Decode(Stego):
    #Define an init function within 'Decode'
    def __init__(self,Object,output):
        #Store the user inputs within variables
        self.object = Object
        self.output = output
        #Open the stego object image
        self.object_open = Image.open(Object)
        #Get the size of the stego object image
        self.object_size = self.object_open.size
        #Calculate the size of the hidden image
        self.hidden_size = ((int(self.object_size[0] / 2)),(int(self.object_size[1] / 2)))
        #Create an instance of 'ImageAnalyser' for the selected stego object
        self.object_RGB = self.ImageAnalyser(self.object)
        #Create an instance of 'ArrayConverter' for the array returned by 'ImageAnalyser'
        self.object_bin = self.ArrayConverter(self.object_RGB)

        #Define a new function called 'ImageDecoder'
        def ImageDecoder(self,Object,output):
            #Create a new, blank image
            self.make = Image.new('RGB', self.hidden_size, 'white')
            #Create two new, empty arrays
            self.hidden_seq = []
            self.hidden_array = []
            #Create a variable called time
            self.time = 12

            #Create an iteration for each value in the length of 'object_bin'
            for j in range(len(self.object_bin)):
                #Store each value in a variable
                self.object_val = self.object_bin[j]
                #Select the last two bit of each value
                self.val = self.object_val[6:8]
                #Append the last two bits to 'hidden_seq'
                self.hidden_seq.append(self.val)

            #Create an iteration for each value in the length of 'hidden_seq'
            for k in range(0,len(self.hidden_seq),12):
                #Select twelve values from 'hidden_seq'
                self.bit = self.hidden_seq[k:self.time]
                #Concatenate the first four values
                self.bit_RGB_1 = self.bit[0]+self.bit[1]+self.bit[2]+self.bit[3]
                #Concatenate the next four values
                self.bit_RGB_2 = self.bit[4]+self.bit[5]+self.bit[6]+self.bit[7]
                #Concatenate the last four values
                self.bit_RGB_3 = self.bit[8]+self.bit[9]+self.bit[10]+self.bit[11]
                #Cast the three 8-bit binary sequences to decimal
                self.bit_RGB_1 = int(self.bit_RGB_1, 2)
                self.bit_RGB_2 = int(self.bit_RGB_2, 2)
                self.bit_RGB_3 = int(self.bit_RGB_3, 2)
                #Cast a list of the three decimal values to a tuple
                self.tuple = tuple([self.bit_RGB_1,self.bit_RGB_2,self.bit_RGB_3])
                #Append the tuple to 'hidden_array'
                self.hidden_array.append(self.tuple)
                #Increase time by 12
                self.time +=12

            #Add the data from 'hidden_array' to the blank image
            self.im = self.make.putdata(self.hidden_array)
            #Save the image with the new data added
            self.im = self.make.save(output)

        #Create an instance of the 'ImageDecoder' function
        decoded = ImageDecoder(self,Object,output)

#Create an instance of the 'Encode' class
Im_Encoded = Encode('cover.bmp','hide.bmp','object.bmp')
#Create an instance of the 'Decode' class
Im_Decoded = Decode('object.bmp','retrieved.bmp')
