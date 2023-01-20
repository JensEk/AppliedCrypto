import re

alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#"
readWords = {}
readLetters = {}
newlineWord = ""


with open("ctext1.txt", "r", encoding='UTF-8') as file:
    for line in file:
        words = re.split(r'_|#', line)
        for word in words:
            if (len(word) > 0 and word[-1] == '\n'):
                newlineWord = word[:-1]
            else:
                word = newlineWord + word
                for letter in word: 
                        if letter in readLetters:
                            readLetters[letter] += 1
                        else:
                            readLetters[letter] = 1
                
                if word in readWords:
                    readWords[word] += 1
                elif word != '':
                    readWords[word] = 1
                newlineWord = ""


print("Words: ", sorted(list(readWords.keys()), key = len))
print("Wordcount: ", readWords)
print("Lettercount: ", sorted(readLetters.items()))