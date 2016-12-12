import io, json
import uniout
# -*- coding: utf-8 -*-

result = []

with io.open("wordutf.txt", "r", encoding="UTF-8") as inputFile:
    for line in inputFile:
        element = line.split(" ")
        if len(element) > 3:
            print line
            print element
            result.append(element)


with io.open("data.txt", "w", encoding="utf-8") as f:
    f.write(unicode(json.dumps(result, ensure_ascii=False)))

