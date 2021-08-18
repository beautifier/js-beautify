def sortDict(tempDict):
    tempKeys = list(tempDict.keys())

    tempKeys = sorted(tempKeys)

    newdict1 = {}
    for i in range(len(tempKeys)):
        newdict1[tempKeys[i]] = tempDict[tempKeys[i]]
        tempDict.pop(tempKeys[i])

    return newdict1


def sortJSON(newdict):

    dictKeys = list(newdict.keys())
    if(len(dictKeys) == 0):
        return {}
    for i in range(len(dictKeys)):
        if(type(newdict[dictKeys[i]]) == dict):
            sortJSON(newdict[dictKeys[i]])
            newdict[dictKeys[i]] = sortDict(newdict[dictKeys[i]])

    return newdict


def main():

    newDict = {
        "b": "b",
        "c": {
            "b": {
                "c": "cc",
                "b": "bb",
                'a': "aa",
            },
            "a": "a"
        },
        "a": ["array", "not", "affected"]
    }

    print(sortDict(sortJSON(newDict)))


main()
