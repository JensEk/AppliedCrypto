#!/usr/bin/env python3

alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#"     # 38 characters in total


# frequency analysis
def analyseLetters(readLetters):
    sortedLetters = sorted(readLetters.items(), key= lambda x:x[1], reverse=True)        
    print("Lettercount: ", sortedLetters)
    for letter in sortedLetters:
        print("Frequency of ", letter[0], ": ", round(letter[1]/sum(readLetters.values()), 5))
    print()
    return sortedLetters[0:2]

# Manuell bruteforce for most common letter in english "e" and "_"
# encryption = (plaintext + key) % 38
# Y(34) = ( _(36) + -2 || 36 ) % 38
# S(28) = ( _(36) + -8 || 30 ) % 38

# Y(34) = ( e(14) + -18 || 20 ) % 38
# S(28) = ( e(14) + -24 || 14 ) % 38

def bruteCeasar(cipher):
    print(f"Bruteforcing ceasar cipher: {cipher}")
    for key in range(1, len(alphabet)):
        shiftedWord = ""
        for c in cipher:
            shiftedWord += alphabet[((alphabet.find(c) - key)%len(alphabet))]
       
        print(f"Cipher shifted {key} times:", shiftedWord)
    print()  

# Try swapping the most common letter with "e" and "|" to represent _ and see if it makes sense
def analyseSubstitution(cipher, topletters):
    
    swapFirst = cipher[0:100].replace(topletters[0][0], "|").replace(topletters[1][0], "e")
    swapSecond = cipher[0:100].replace(topletters[0][0], "e").replace(topletters[1][0], "|")
    print(f"Bruteforcing substitution cipher: {cipher[0:100]}")
    print(f"Substituted {topletters[0][0]} with | and {topletters[1][0]} with e : {swapFirst}")
    print(f"Substituted {topletters[0][0]} with e and {topletters[1][0]} with | : {swapSecond}")
    print()
    select = input("Select first or second: ")
    
    if select == "first":
        print(f"Swapping {topletters[0][0]} with | and {topletters[1][0]} with e")
        swapCipher = cipher.replace(topletters[0][0], "|").replace(topletters[1][0], "e")
    elif select == "second":
        print(f"Swapping {topletters[0][0]} with e and {topletters[1][0]} with |")
        swapCipher = cipher.replace(topletters[0][0], "e").replace(topletters[1][0], "|")
    
    readWords = analyzeWords(swapCipher)
    return (swapCipher, readWords)
    
def analyzeWords(swapCipher):
    
    readWords = {}
    commonDoubles = {}
    
    for word in swapCipher.split("|"):
        if word in readWords:
            readWords[word] += 1
            for doubles in commonDoubles:
                if doubles in word:
                    commonDoubles[doubles] += 1 
        else:
            readWords[word] = 1
            for i in range(len(word)-1):
                if word[i] == word[i+1]:
                    commonDoubles[word[i:i+2]] = 1
                    
    readWords = sorted(readWords.items(), key= lambda x:(len(x[0]), x[1]), reverse=True)
    for word in readWords:
        print(str(word).replace("(", "").replace(")", ""))
    print()
    print("Common doubles: ", commonDoubles)
    return readWords

def swapLetter(swapCipher, readWords):
    
    cont = "y"
    copyCipher = swapCipher
    copyWords = readWords
    history = []
    while cont == "y":
        x,y = input("Enter letters to swap X -> y: ").split()
        copyCipher = copyCipher.replace(x, y)
        for word in copyWords:
            if x in word[0]:
                copyWords[copyWords.index(word)] = (word[0].replace(x, y), word[1]) 
    
        print(f"Words after {x}->{y} : ")
        for word in copyWords:
            print(str(word).replace("(", "").replace(")", ""))
        print()
        print(f"Cipher after {x}->{y} : \n", copyCipher[0:700], "\n")
        
        
        choice = input("Keep? (y/n): ")
        if choice == "n":
            copyCipher = copyCipher.replace(y, x)
            for word in copyWords:
                if y in word[0]:
                    copyWords[copyWords.index(word)] = (word[0].replace(y, x), word[1])
            print(f"Cipher after {x}->{y} : \n", copyCipher[0:700], "\n")
        else:
            history.append((x,y))
            print("History: ", history)
        
        cont = input("Continue? (y/n): ")
        if cont == "n":
            return copyCipher.replace("|", " ").replace("\n").upper()

def main():
    readLetters = {}
    cipherText = ""
    
    textFile = input("Enter crypto filename: ")
    
    with open(textFile, "r", encoding='UTF-8') as file:
        for line in file:
            if line[-1] == '\n':
                cipherText += line[:-1]
            else:
                cipherText += line

        for letter in cipherText:
            if letter in readLetters:
                readLetters[letter] += 1
            else:
                readLetters[letter] = 1
    file.close()        
    mostCommon = analyseLetters(readLetters)
    
    cipherType = input("Ceasar or substitution? (c/s): ")
    if cipherType == "c":
        bruteCeasar(cipherText[0:70])
    else:
        swappedCipher, readWords = analyseSubstitution(cipherText, mostCommon)
        finalCipher = swapLetter (swappedCipher, readWords)

    print(finalCipher)
    wrt = input("Write to file? (y/n): ")
    if wrt == "y":
        with open("decrypted.txt", "w") as outfile:
            outfile.writelines(finalCipher)
            outfile.close()
    
    
    
    solution = [('K', 'a'), ('_', 'i'), ('6', 'm'), ('R', 'n'), ('7', 'd'), ('1', 't'), ('F', 'h'), ('Z', 'r'), ('N', 'l'), ('Q', 'w'), ('A', 'o'), ('B', 'f'), ('W', 'g'), ('M', 'u'), ('5', 'v'), ('I', 's'), ('3', 'b'), ('U', 'y'), ('O', 'c'), ('D', 'z'), ('9', 'x'), ('V', 'p'), ('E', 'q'), ('J', 'j'), ('2', 'k'), ('L', '1'), ('4', '2'), ('P', '3'), ('8', '4'), ('T', '5'), ('C', '6'), ('X', '7'), ('G', '8'), ('#', '9'), ('H', '#')]

if __name__ == "__main__":
    main()