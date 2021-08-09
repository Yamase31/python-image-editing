"""
Author: Ken Lambert
File: testimages.py
Project 8

Script for testing image processing functions.
"""

from images import Image

# Functions that transform images

def blackAndWhite(image):
    """Converts image to black and white."""
    blackPixel = (0, 0, 0)
    whitePixel = (255, 255, 255)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (r, g, b) = image.getPixel(x, y)
            average = (r + g + b) // 3
            if average < 128:
                image.setPixel(x, y, blackPixel)
            else:
                image.setPixel(x, y, whitePixel)

def detectEdges(image, amount):
    """Builds and returns a new image in which the 
    edges of the argument image are highlighted and
    the colors are reduced to black and white."""

    def average(triple):
        (r, g, b) = triple
        return (r + g + b) // 3

    blackPixel = (0, 0, 0)
    whitePixel = (255, 255, 255)
    new = image.clone()
    y = 0
    for y in range(image.getHeight() - 1):
        for x in range(1, image.getWidth()):
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

# Tester functions

def testBlackAndWhite(name = "smokey.gif"):
    """Loads and draws an image, then
    converts it to black and white and redraws it."""
    image = Image(name)
    print("Close the image window to see the transformation")
    image.draw()
    blackAndWhite(image)
    image.draw()

def testDetect(name = "smokey.gif", amount = 20):
    """Loads and draws an image, then
    detects edges and redraws it."""
    image = Image(name)
    print("Close the image window to see the transformation")
    image.draw()
    image2 = detectEdges(image, amount)
    image2.draw()

# Code to run a tester function

def main(name = "smokey.gif"):
    testBlackAndWhite(name)
##    testDetect(name)

if __name__ == "__main__":
    main()
        
