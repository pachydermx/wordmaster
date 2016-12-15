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
                id = leftSide[0]
                word = leftSide[1]
                rightSide = stepTwo[1].split(".")
                equ = rightSide[0] + "."
                desS = stepTwo[1].split(" ")
                des = desS[-1]
                # after
                print [id, word, equ, des]
                types = [' adv.', ' adj.', ' n.', ' v.', ' ad.', ' a.', ' vi.', ' vt.']
                for type in types:
                    if equ.find(type) > 0:
                        des = " " + type + des
                        equ = equ.replace(type, "")
                des = des.replace('\n', '')
                result.append([id, word, equ, des])
                print [id, word, equ, des]
            else :
                result.append(element)


with io.open("data.txt", "w", encoding="utf-8") as f:
    f.write(unicode(json.dumps(result, ensure_ascii=False)))

