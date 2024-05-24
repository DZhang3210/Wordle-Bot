def createPrefix():
    wordList = open("wordList.txt", "r")
    data = wordList.read()
    words = data.split("\n")
    prefix = {}
    curr = prefix
    for word in words:
        for c in word:
            index = ord(c) - ord('a')
            if index not in curr:
                curr[index] = {}
            curr = curr[index]
        curr = prefix
    wordList.close()
    return [words, prefix]

def prefixCheck(prefix, word):
    for c in word:
        if c not in prefix:
            return False
        prefix = prefix[c]
    return True

# import random
# words = createPrefix()[0]
# w = words[int(random.random() * len(words))]
# print(w)
# print([ord(c) - ord('a') for c in w])