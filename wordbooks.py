# Only one letter conversions here. The number represents the special
# letter. It's gotten by pythons 'ord("letter")' function.
converse1 = {
    192: "A",
    193: "A",
    194: "A",
    195: "A",
    197: "A",
    199: "C",
    200: "E",
    201: "E",
    202: "E",
    203: "E",
    204: "I",
    205: "I",
    206: "I",
    207: "I",
    208: "D",
    209: "N",
    210: "O",
    211: "O",
    212: "O",
    213: "O",
    216: "O",
    217: "U",
    218: "U",
    219: "U",
    268: "C",
    327: "N",
    270: "D",
    356: "T",
    344: "R",
    221: "Y",
    366: "U",
    282: "E",
    352: "S",
    381: "Z",
    321: "L",
    346: "S",
    280: "E",
    377: "Z",
    379: "Z",
    260: "A",
    323: "N",
    262: "C",
    45: "["
}
# All multi letter conversions here.
converse2 = {
    196: "AE",
    198: "AE",
    214: "OE",
    220: "UE",
    338: "OE"
}


def wordbooks_ask(minlength, maxlength, namelist, convert):
    """
    This function converts wordlists in namelist[i] ".txt" format to python
    lists.
    It converts all letters to Uppercase A-Z. Strange letters get converted as
    determined in converse1+2 dict. If not defined the whole word gets deleted.
    The .txt files should be formatted in "utf_8" and single words have to be
    split by paragraphs equivalent to "\n".

    "count" is the number of wordlists. Make sure that enough files formatted
    like 0.txt 1.txt etc. are existent.

    "minlength" is the minimum count of letter per word, less and the word
    gets deleted.

    "maxlength" it the maximum count of letters per word, more and the word
    gets deleted.
    """
    print("Starting conversion of Wordlists!")

    wb = []
    for i in range(len(namelist)):
        wordbook = open(str(namelist[i]) + ".txt", "rb").read()
        wordbook = wordbook.decode("utf_8")
        if convert is True:
            wordbook = wordbook.upper()
        wordbook = wordbook.split("\n")

        if maxlength > 0:
            # only checking for maxlength since the words can grow via the
            # multi letter conversions
            wordbook = [word for word in wordbook if len(word) <= maxlength]
        if convert is True:
            killlist = []
            # wordbook[j] = word
            # wordbook[j][k] = letter of word
            for j in range(len(wordbook)):
                strangelist = []
                for k in range(len(wordbook[j])):
                    index = ord(wordbook[j][k])
                    if index < 65 or index > 90:
                        if index in converse1:
                            wordbook[j] = (wordbook[j][:k]
                                           + converse1[index]
                                           + wordbook[j][k + 1:])
                        elif index in converse2:
                            strangelist.append((j, wordbook[j][k]))
                        else:
                            killlist.append(j)
                            break
            # Multi Letter conversions have to be dealt with seperately, since
            # they shift the Letters to the right, messing up the loops and
            # going over the max letter count.
            #
            # Instead of simply swapping the letters, this loop searches for
            # the given "strange" letter every time and doesn't care about the
            # individual position. Hence it checks the final length and
            # deletes.
                for w in strangelist:
                    index = wordbook[w[0]].index(w[1])
                    wordbook[w[0]] = (wordbook[w[0]][:index]
                                      + converse2[ord(wordbook[w[0]][index])]
                                      + wordbook[w[0]][index + 1:])

            for l in range(len(killlist)):
                wordbook.pop(killlist[l] - l)

        # final trimming to desired word length
        if minlength > 0:
            wordbook = [w for w in wordbook if len(w) >= minlength]
        if maxlength > 0:
            wordbook = [w for w in wordbook if len(w) <= maxlength]

        wordbook = [word + "[" for word in wordbook]
        wb.append(wordbook)
        print("Conversed Wordlist " + str(namelist[i]) + " with "
              + str(len(wordbook)) + " words")
    print("Conversion Done ")
    return wb


def convert_word(minlength, maxlength, word, convert):
    """
    This function converts the given word to all uppercase A-Z format. If it's
    too long, everything past maxlength will be cut off. If it's too short,
    "A"s will be added until minlength is reached.
    """
    if convert is True:
        strangelist = []
        killlist = []
        word = word.upper()
        for i in range(len(word)):
            code = ord(word[i])
            if code < 65 or code > 90:
                if code in converse1:
                    word = (word[:i] + converse1[code] + word[i + 1:])
                elif code in converse2:
                    strangelist.append(word[i])
                else:
                    killlist.append(word[i])

        for i in strangelist:
            index = word.index(i)
            word = (word[:index] + converse2[ord(i)] + word[index + 1:])

        for i in killlist:
            index = word.index(i)
            word = (word[:index] + word[index + 1:])

    if maxlength > 0 and len(word) > maxlength:
        word = word[:maxlength]

    elif minlength > 0 and len(word) < minlength:
        word = (word + (minlength - len(word)) * "A")

    return(word + "[")


def check_all():
    """
    This function checks for foreign Letters in a given wordlist

    It should be used to determine if the converse1 and 2 dicts should be
    extended for the use in the new language.

    Same rule as in the actual import exist here. Words have to be seperated
    by \n and the text has to be in utf_8 format.
    """
    converse = dict()
    converse.update(converse1)
    converse.update(converse2)

    print("Now checking if foreign letters in language file are translated "
          "in converse1 and 2 dict to A-Z.")
    print("")
    print("Words in list have to be seperated by newlines.")
    print("File should be .txt and utf_8 format.")
    print("Please enter filename without .txt ending.")
    name = input("Filename: ")
    wordbook = open(name + ".txt", "rb").read()
    wordbook = wordbook.decode("utf_8")
    wordbook = wordbook.upper()
    wordbook = wordbook.split("\n")

    # wordbook[j] = word
    # wordbook[j][k] = letter of word
    strangeset = set()
    for j in range(len(wordbook)):
        for k in range(len(wordbook[j])):
            index = ord(wordbook[j][k])
            # Check if letter is in range and in converse dict.
            if index < 65 or index > 90:
                if index not in converse:
                    strangeset.add(wordbook[j][k])
    strangelist = list(strangeset)
    if len(strangelist) == 0:
        print("All strange letters are in the conversion list!")
    else:
        print("Following letters are not in the conversion list")
        for i in strangelist:
            print(i + " ord:" + str(ord(i)))
        print("Words with one of these letters in it "
              "will be ignored by Neurons.")


def check_word(minlength, maxlength, word, convert):
    """
    Checks if given word is properly formatted as it would be after being
    imported by the wordbooks function.
    """
    if minlength > 0 and len(word) < minlength or \
       maxlength > 0 and len(word) > maxlength:
        return(False)
    if convert is True:
        for i in range(len(word)):
            index = ord(word[i])
            # Check if letter is in A-Z range.
            if index < 65 or index > 91:
                return(False)
    return(True)


if __name__ == "__main__":
    check_all()
