# Authored by: Jacob Houck.
# I hereby state that this entire program is my own work.
# November 16, 2017
# CS424-02
# This program implements the vertical and horizonal flip filters, the invert colors filter, and the color flattening filter.
#It asks for a filename, loads the file, asks which filters to apply, and then saves the altered image.
#I use a Pixel class, a Line class, and an Image class.

class Pixel:#Holds one pixel.
    def __init__(self, colors):
        #We split the list of colors into seperate entries.
        self.red = colors[0]
        self.green =colors[1]
        self.blue = colors[2]
    def toString(self):
        #Converts pixels to a string for use in saving or displaying the image data
        thestring = str(self.red) +" "+str(self.green) +" "+str(self.blue)
        return thestring
    def printPixel(self):
        
        print(str(self.red) +" "+str(self.green) +" "+str(self.blue))
        
    def flattenBlue(self):
        self.blue = 0;
    def flattenRed(self):
        self.red = 0;
    def flattenGreen(self):
        self.green = 0;
    def invertColors(self):
        self.green = abs(self.green-255)
        self.red = abs(self.red-255)
        self.blue = abs(self.blue-255)

class Line:
    
    def __init__(self,line):
        self.pixels = []
        self.setLine(line)
    def setLine(self, line):
        
        line = str.split(line)
        #Now we split the line into pixels.
        x=0
        colors=[1,2,3];
        for color in line:
            x=x+1
            if (x==1):
                colors[0] = int(color)
            elif(x==2):
                colors[1] = int(color)
            elif(x==3):#If this is true, we have Red, Green, and Blue, so we can create a new Pixel and add it to our pixel list.
                colors[2]= int(color)
                x=0
                self.pixels.append(Pixel(colors))
                
    def flattenBlue(self):
        for x in self.pixels:
            x.flattenBlue()
            
    def horizontal_flip(self):
        self.pixels.reverse()
    def flattenRed(self):
        for x in self.pixels:
            x.flattenRed()
            
    def flattenGreen(self):
        for x in self.pixels:
            x.flattenGreen()
            
    def getLine(self):
        return self.pixels
    #def printLine(self):
        #for x in self.pixels:
            #print(x.printPixel())
    def invertColors(self):
        for x in self.pixels:
            x.invertColors()
            
class Image:
    def printImage(self):
        for x in self.lines:
            x.printLine();
            
    def save(self):
        timeForNewLine = 0;
        savefile=open("FilteredImage.ppm", "w")
        #Save header first.
        savefile.write(self.header)
        #print(self.lines[::])
        for line in self.lines:
            #print(line.pixels[::])
            for pixel in line.pixels:
                 #print(pixel.toString())
                 savefile.write(pixel.toString()+" ")
                 timeForNewLine = timeForNewLine + 1;
                 if(timeForNewLine==int(self.width)):#If we have reached the end of the line.
                     savefile.write("\n")
                     #print("OH YEAH!")
                     timeForNewLine = 0;
                     
        savefile.close()
        
    def __init__(self, filename):
        #This opens the file, and calls load
        self.lines = []#Holds lines of the image
        self.load(filename)

    def load(self, filename):
        first = 1;
        with open(filename) as f:
            if(first==1):#First loop, so we save the header
                self.header = next(f)
                tempheader = next(f)#This contains the size data.
                temp = str(tempheader); # In these next few lines, we manipulate to get just the size data we need.
                temp = temp.split()
                self.width = int(temp[0])
                
                self.header = self.header + tempheader
                self.header = self.header + next(f)

            for line in f:
                self.lines.append(Line(line))
            
    def flattenBlue(self):
        #print("Flattening...")
        for pixel in self.lines:
            pixel.flattenBlue()
            
    def flattenRed(self):
        #print("Flattening...")
        for pixel in self.lines:
            pixel.flattenRed()
            
    def flattenGreen(self):
        #print("Flattening...")
        for pixel in self.lines:
            pixel.flattenGreen()
    def invertColors(self):
        #print("Invering colors...")
        for pixel in self.lines:
            pixel.invertColors()
        
    def horizontal_flip(self):
        #print("Fliping Horizanally...")
        for line in self.lines:
            line.horizontal_flip()
        
    
    def vertical_flip(self):
        #We only need to call the Python built-in reverse function on the Lines list to accomplish this.
        self.lines.reverse()
    
                
                
        
#Beginning of Execution
print("Welcome to my image filtering program!")

filename = input("Please enter the name of the image you would like to manipulate: ")
image = Image(filename)

if((input("\nWould you like to flip the image horizontally? Type y for yes, and any other key for no: "))=='y'):
    image.horizontal_flip()
    
if((input("\nWould you like to flip the image vertically? Type y for yes, and any other key for no: "))=='y'):
    image.vertical_flip()
    
if((input("\nWould you like to invert colors? Type y for yes, and any other key for no: "))=='y'):
    image.invertColors()
if((input("\nWould you like to flatten blue? Type y for yes, and any other key for no: "))=='y'):
    image.flattenBlue()
if((input("\nWould you like to flatten green? Type y for yes, and any other key for no: "))=='y'):
    image.flattenGreen()
if((input("\nWould you like to flatten red? Type y for yes, and any other key for no: "))=='y'):
    image.flattenRed()

print("\nSaving file as 'FilteredImage.ppm'")

image.save()#Saves the image

print("\nThank you for my filtering program :)")

