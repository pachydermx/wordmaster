import io, json
import uniout
# -*- coding: utf-8 -*-

result = []

with io.open("wordutf.txt", "r", encoding="UTF-8") as inputFile:
    for line in inputFile:
        element = line.split(" ")
        if len(element) > 3:
            stepTwo = line.split("=")
            if len(stepTwo) > 1:
                leftSide = stepTwo[0].split(".")
                print leftSide[1]
                id = leftSide[0]
                word = leftSide[1]
                rightSide = stepTwo[1].split(".")
                equ = rightSide[0]
                desS = stepTwo[1].split(" ")
                des = desS[-1]
                result.append([id, word, equ, des])
            else :
                print line
                print element
                result.append(element)


with io.open("data.txt", "w", encoding="utf-8") as f:
    f.write(unicode(json.dumps(result, ensure_ascii=False)))

