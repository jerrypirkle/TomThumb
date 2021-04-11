#!/usr/bin/env python3
"""
__author__ = "Jerry Pirkle"
__copyright__ = "Copyright (c) 2021 Jerry Pirkle"
__credits__ = ["Jerry Pirkle"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Jerry Pirkle"
__email__ = "jerrypirkle@gmail.com"
__status__ = "Development"

Requirements and Usage:
- Requires Python 3.5+ for glob library
- Install ffmpeg
    -  Mac: brew install ffmpeg
    -  Apt: sudo apt install ffmpeg
    -  Yum: sudo yum install ffmpeg ffmpeg-devel
- Update the Configuration Options
    - inputPath is the root location of the video files. The trailing path is currently required
    - outputPath is the root location of the thumbnail files. The inputPath directory structure is left intact. The trailing path is currently required
"""

import glob
import subprocess

# Configuration Options
inputPath = "samplefiles/"
    # This should be the parent directory of the video files, needs a trailing path directory/
outputPath = "thumbnails/"
    # Directory that you will store the thumbnails in, needs a trailing path directory/

def main():
    """ Main entry point of the app """
    directoryList = getDirectories()

    # Recursively get a list of directories in the inputPath and create the directories in the outputPath because ffmpeg can't do this.
    createDirectories(directoryList)

    # Recursively get a list of files and create thumbnails in the outputPath while preserving the directory structure. Ignore directories in processing.
    for filename in getFiles():
        if filename in directoryList:
            print("Skipping Directory: " + filename)
        else:
            print("Processing: " + filename)
            # Process thumbnails
            thumbnailProcess(filename)



def getDirectories():
    """ Get a list of subdirectories from the inputPath.  """
    directoryOutputList = []
    # recursively search inputPath and add directories to a list
    for filename in glob.iglob(inputPath + '**/', recursive=True):
        directoryOutputList.append(filename)
    return directoryOutputList



def createDirectories(directoryList):
    """ Takes a list of directories and creates the directories in the outputPath """
    for directory in directoryList:
        subprocess.call(['mkdir', '-p', outputPath + directory])



def getFiles():
    """ Returns a list of all files in the inputPath"""
    fileOutputList = []
    # Use glob to find all the pathnames matching a specified pattern according to the rules used by the Unix shell, https://docs.python.org/3.5/library/glob.html#glob.glob
    for filename in glob.iglob(inputPath + '**/**', recursive=True):
        fileOutputList.append(filename)
    # fileOutputList.remove(inputPath)
    return fileOutputList



def thumbnailProcess(filename):
    """ Takes a video filename as input and outputs a thumbnail """
    outputFile = outputPath + filename + '.jpg'
    # generate thumbnails
    subprocess.call(['ffmpeg', '-i', filename, '-ss', '00:00:00.000', '-vframes', '1', outputFile, '-y'])



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
