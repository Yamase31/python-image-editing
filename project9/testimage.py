"""
Created by Beth Ann Townsend and James Lawson
File: testimages.py
Project 9

This program holds functions used for editing an image and allows them to be
tested one-by-one.
"""

from images import Image
import random
import math

#The following are functions that edit the image:


def grayScale(image): #changes to gray scale
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (red, green, blue) = image.getPixel(x, y)
            #using the luminence scale to trick the eye:
            red = int(red * .299)
            green = int(green * .587)
            blue = int(blue * .114)
            gray = red + green + blue
            image.setPixel(x, y, (gray, gray, gray))

def posterize(image, randomPixel): #changes the image to a random color and white
    randomPixel = ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    whitePixel = (255, 255, 255)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (r, g, b) = image.getPixel(x, y)
            average = (r + g + b) // 3
            if average < 128:
                image.setPixel(x, y, randomPixel)
            else:
                image.setPixel(x, y, whitePixel)


def colorscale(image): #edits the coloring of an image to a random color and black
    randomR = random.randint(0, 255)
    randomG = random.randint(0, 255)
    randomB = random.randint(0, 255)
    blackPixel = (0, 0, 0)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (r, g, b) = image.getPixel(x, y)
            r = (r + randomR) / 2
            r = int(r * .299)
            g = (g + randomG) / 2
            g = int(g * .587)
            b = (b + randomB) / 2
            b = int(b * .114)
            gray = r + g + b #not truly gray, but following the format of the above for ease
            image.setPixel(x, y, (gray, gray, gray))


def sepia(image): #turns the picture to look like sepia
    grayScale(image)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (red, green, blue) = image.getPixel(x, y)
            #color amounts to turn it that sepia color
            if red < 63:
                red = int(red * 1.1)
                blue = int(blue * 0.9)
            elif red < 192:
                red = int(red * 1.15)
                blue = int(blue * 0.85)
            else:
                red = min(int(red * 1.08), 255)
                blue = int(blue * 0.93)
            image.setPixel(x, y, (red, green, blue))


def blackAndWhite(image): #converts image to black and white
    blackPixel = (0, 0, 0)
    whitePixel = (255, 255, 255)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (r, g, b) = image.getPixel(x, y)
            average = (r + g + b) // 3
            if average < 128: #from the halfway point since black is 0 and white is 255
                image.setPixel(x, y, blackPixel)
            else:
                image.setPixel(x, y, whitePixel)

def detectEdges(image, amount): #function used in sharpen to analyze the colors of the surrounding pixels
    def average(triple): #function to calculate the average so we can call it down the line
        (r, g, b) = triple
        return (r + g + b) // 3

    blackPixel = (0, 0, 0)
    whitePixel = (255, 255, 255)
    new = image.clone()
    y = 0
    for y in range(image.getHeight() - 1):
        for x in range(1, image.getWidth()):
            #the part that looks to the pixels around it
            oldPixel = image.getPixel(x, y)
            leftPixel = image.getPixel(x - 1, y)
            bottomPixel = image.getPixel(x, y + 1)
            oldLum = average(oldPixel)
            leftLum = average(leftPixel)
            bottomLum = average(bottomPixel)
            if abs(oldLum - leftLum) > amount or \
               abs(oldLum - bottomLum) > amount:
                new.setPixel(x, y, blackPixel)
            else:
                new.setPixel(x, y, whitePixel)
    return new

def sharpen(image, amount, degree): #"sharpens" the picture, making it more harsh to a certain degree
    def average (pixel):
        (r, g, b) = pixel
        return (r + g + b) // 3
    width = image.getWidth() - 1
    height = image.getHeight() - 1
    newImage = image.clone()
    for y in range (1, height):
        for x in range(1, width):
            (r, g, b) = image.getPixel(x, y)
            #again checking the bordering pixels
            oldPixel = image.getPixel(x, y)
            leftPixel = image.getPixel(x - 1, y)
            bottomPixel = image.getPixel(x, y + 1)
            oldLum = average(oldPixel)
            leftLum = average(leftPixel)
            bottomLum = average(bottomPixel)
            if abs(oldLum - leftLum) > amount or \
               abs(oldLum - bottomLum) > amount:
                newImage.setPixel(x, y, (int(max(0, oldPixel[0]*(1-degree))), int(max(0, oldPixel[1]*(1-degree))), int(max(0, oldPixel[2]*(1-degree)))))
     
            else:
                #safe-guard that keeps the amount at or below 255 so it doesn't exceed the possible color value
                if amount > 255:
                    newPixel == 255
                newImage.setPixel(x, y, (int(min(255, oldPixel[0]*(1+degree))), int(min(255, oldPixel[1]*(1+degree))), int(min(255, oldPixel[2]*(1+degree)))))
    return newImage                            

def rotateRight(image): #rotates the image 90 degrees clockwise by first reversing x and y
    newImage = Image(image.getHeight(), image.getWidth())
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            oldPixel = image.getPixel(x, y) 
            newImage.setPixel(image.getHeight() - y - 1, x, oldPixel)
    return newImage
    

#these are the functions that test the functions above
def testPosterize(name = "smokey.gif"): #tests posterize
    randomPixel = ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    whitePixel = (255, 255, 255)
    image = Image(name)
    print("Close the image window to see the transformation!")
    image.draw()
    posterize(image, randomPixel) #calls it here
    image.draw()

def testColorscale(name = "smokey.gif"): #tests colorscale
    randomPixel = ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    whitePixel = (255, 255, 255)
    image = Image(name)
    print("Close the image window to see the transformation!")
    image.draw()
    colorscale(image) #calls it here
    image.draw()

def testSepia(name = "smokey.gif"): #tests sepia
    image = Image(name)
    print("Close the image window to see the transformation!")
    image.draw()
    sepia(image) #calls it here
    image.draw()
    
def testSharpen(name = "smokey.gif"): #tests sharpen
    image = Image(name)
    print("Close the image window to see the transformation!")
    image.draw()
    amount = 20
    degree = .2
    image2 = sharpen(image, amount, degree) #calls it here
    image2.draw()

def testBlackAndWhite(name = "smokey.gif"): #blackandwhite test
    """Loads and draws an image, then
    converts it to black and white and redraws it."""
    image = Image(name)
    print("Close the image window to see the transformation")
    image.draw()
    blackAndWhite(image) #calls it here
    image.draw()

def testDetect(name = "smokey.gif", amount = 20): #tests detectedges
    """Loads and draws an image, then
    detects edges and redraws it."""
    image = Image(name)
    print("Close the image window to see the transformation")
    image.draw()
    image2 = detectEdges(image, amount) #calls it here
    image2.draw()

def testRotateRight(name = "smokey.gif"): #tests rotateright
    image = Image(name)
    print("Close the image window to see the transformation!")
    image.draw()
    image2 = rotateRight(image) #calls it here
    image2.draw()


#this code runs a tester function

def main(name = "smokey.gif"):
    testColorScale(name)
#    here, call the test function for the function you wish to check ^^^

if __name__ == "__main__":
    main()
