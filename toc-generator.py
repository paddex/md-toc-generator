#!/usr/bin/python3

import sys
import json
import os.path

class TocGenerator:

    def __init__(self, inF, outF):
        self.inF = inF
        self.outF = outF

    def gen(self):
        with inF:
            lines = inF.readlines()

        self.setHeadingFormat(lines)
        self.genLinks(lines)
        self.genToc()

    def genLinks(self, lines):
        firstLevelCounter = 0
        secondLevelCounter = 0
        self.headings = []
        self.newLines = []

        for line in lines:

            if line.startswith("#"):
                if line.startswith(self.secondLevel):
                    secondLevelCounter += 1
                elif line.startswith(self.firstLevel):
                    firstLevelCounter += 1
                    secondLevelCounter = 0
                    
                name = str(firstLevelCounter) + "." + str(secondLevelCounter)

                lineTmp = line.replace("#", "")
                lineTmp = lineTmp.strip()

                self.appendToHeadings(line, lineTmp, name)

                link = "<a name='" + name + "'></a>"
                self.newLines.append(link)

            self.newLines.append(line)

    def genToc(self):
        pass

    def output(self, text):
        print(text, file=self.outF)


    def appendToHeadings(self, line, heading, link):
        if line.startswith(self.secondLevel):
            subHeadingDict = {
                "heading" : heading,
                "link" : link
            }
            self.headings[-1]["subs"].append(subHeadingDict)
        elif line.startswith(self.firstLevel):
            headingDict = {
                "heading" : heading,
                "link" : link,
                "subs" : []
            }
            self.headings.append(headingDict)

    def setHeadingFormat(self, lines):
        firstLevelCounter = 0
        secondLevelCounter = 0
        thirdLevelCounter = 0
        foundLevel = False

        for line in lines:
            if line.startswith("#"):
                if line.startswith("##"):
                    if line.startswith("###"):
                        thirdLevelCounter += 1
                        foundLevel = True

                    if not foundLevel:
                        secondLevelCounter += 1
                        foundLevel = True

                if not foundLevel:
                    firstLevelCounter += 1
                    foundLevel = True

            foundLevel = False

        if firstLevelCounter > 0:
            self.firstLevel = "#"
            self.secondLevel = "##"
        elif secondLevelCounter > 0:
            self.firstLevel = "##"
            self.secondLevel = "###"
        elif thirdLevelCounter > 0:
            self.firstLevel = "###"
            self.secondLevel = "####"



if __name__ == "__main__":

    if len(sys.argv) < 1:
        print("Usage:")
        print("python toc-generator.py <inputfile> [outputfile]")
        sys.exit(1)

    try:
        inputfile = sys.argv[1]
        inF = open(inputfile, "r")
    except IOError:
        print("Error: Could not open file: " + inputfile)
        sys.exit(1)

    try:
        if len(sys.argv) > 2:
            outputfile = sys.argv[2]
            outF = open(outputfile, "w")
        else:
            outF = sys.stdout
    except IOError:
        print("Error: Could not open file: " + outputfile)
        sys.exit(1)

    tocGen = TocGenerator(inF, outF)
    tocGen.gen()
