#!/usr/bin/env python3


# Progam to analyse and decrypt ceasar, substitution and vigenere ciphers.
# Made by: Jens Ekenblad
# Date: 2022-01-26

import math

alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#"     # 38 characters in total
frequencyEng = {"A":"0.072", "B":"0.013", "C":"0.024", "D":"0.037", "E":"0.112", "F":"0.020", "G":"0.018", "H":"0.054", "I":"0.061", "J":"0.001", "K":"0.007", "L":"0.035", "M":"0.021", "N":"0.059", "O":"0.066", "P":"0.017", "Q":"0.001", "R":"0.053", "S":"0.056", "T":"0.080", "U":"0.024", "V":"0.009", "W":"0.021", "X":"0.001", "Y":"0.017", "Z":"0.001", "_":"0.120", }


# Solution for c1.txt
solution1 = [('Y', '|'), ('S', 'e'), ('K', 'a'), ('_', 'i'), ('6', 'm'), ('R', 'n'), ('7', 'd'), ('1', 't'), ('F', 'h'), ('Z', 'r'), ('N', 'l'), ('Q', 'w'), ('A', 'o'), ('B', 'f'), ('W', 'g'), ('M', 'u'), ('5', 'v'), ('I', 's'), ('3', 'b'), ('U', 'y'), ('O', 'c'), ('D', 'z'), ('9', 'x'), ('V', 'p'), ('E', 'q'), ('J', 'j'), ('2', 'k'), ('L', '1'), ('4', '2'), ('P', '3'), ('8', '4'), ('T', '5'), ('C', '6'), ('X', '7'), ('G', '8'), ('#', '9'), ('H', '#')]



# frequency analysis
def analyseLetters(cipherText):
    
    readLetters = {}
    for letter in cipherText:
            if letter in readLetters:
                readLetters[letter] += 1
            else:
                readLetters[letter] = 1
    
    sortedLetters = sorted(readLetters.items(), key= lambda x:x[1], reverse=True)        
    print("Lettercount: ", sortedLetters)
    for letter in sortedLetters:
        print("Frequency of ", letter[0], ": ", round(letter[1]/sum(readLetters.values()), 5))
    print()
    return sortedLetters[0:2]


# column frequency analysis for Vigenere where each column is stepped by the keylength
def analyseColumns(columns):
    
    allCol = []
    underscore = []
    for col in columns:
        
        readLetters = {}
        for letter in col:
                if letter in readLetters:
                    readLetters[letter] += 1
                else:
                    readLetters[letter] = 1
        
        set = {}
        sortedLetters = sorted(readLetters.items(), key= lambda x:x[1], reverse=True)        
        for letter in sortedLetters:
            set[letter[0]] = round(letter[1]/sum(readLetters.values()), 5)
        allCol.append(set)        
        
    for set in allCol:
        underscore.append(list(set.keys())[0])
        print(f"Freq of {allCol.index(set)} : {set}", end="\n\n")  
    
    return underscore
 

        

# Brute shifting the ceasar cipher
def bruteCeasar(cipher):
    print(f"Bruteforcing ceasar cipher: {cipher}")
    solution = []
    for key in range(1, len(alphabet)):
        shiftedWord = ""
        for c in cipher:
            shiftedWord += alphabet[((alphabet.find(c) - key)%len(alphabet))]
        solution.append(shiftedWord)
        print(f"Cipher shifted {key} times:", shiftedWord)
    
    print()
    shift = int(input("Enter which shift to choose: ")) 
    return shift


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
 

# Extract each individual word and count the occurence of each word along with the occurence of common doubles like "dd"    
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
        if word[1] > 2:
            print(str(word).replace("(", "").replace(")", ""))
    print()
    print("Common doubles: ", commonDoubles)
    return readWords


# Manueally swap letters to see if it makes sense and keep the history of swaps
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
            return copyCipher.replace("|", " ").replace("#", "\n").upper()



# Split cipher into sets of size 2-4 and calculate the gcd of the distances between each occurence of the nGram
def vigenereAnalyse(cipher):
    
    nGram = {}
    gcdGlobal = {}
    
    for n in range(2, 5):    
        # Split cipher into nGrams and store the position of each nGram
        for i in range(0, len(cipher)-(n-1)):
            if cipher[i:i+n] in nGram:
                nGram[cipher[i:i+n]].append(i)
            else:
                nGram[cipher[i:i+n]] = [i]
        
        # If nGram occurs more than once, calculate the distance between each occurence and gdc    
        for j in nGram:
            if len(nGram[j]) > 1:
                dst = []
                gcd = []
                for i in range(len(nGram[j])-1):
                    dst.append(nGram[j][i+1] - nGram[j][i])
                    if i > 0:
                        gcd.append(math.gcd(dst[i], dst[i-1]))
            
                #print(f"nGram: {j}:   pos={nGram[j]}    Dst={dst}   GCD={gcd}")
                for g in gcd:
                    if g in gcdGlobal:
                        gcdGlobal[g] += 1
                    else:
                        gcdGlobal[g] = 1
             
    gcdGlobal = sorted(gcdGlobal.items(), key= lambda x:(x[1]), reverse=True)            
    print(f"Most common GCD over all [2-4]Grams (TYPE, AMOUNT): {gcdGlobal[0], gcdGlobal[1]}")
    
    return gcdGlobal[0][0]     



def vigenereCrack(cipher, gcd):
    
    gcdSplit = []
    print("Splitting cipher into columns based on GCD...", "\n")
    for i in range(gcd):
        gcdSplit.append(cipher[i::gcd])
    
    
    ciphMod = ""
    plainText = ""
    history = [""]*len(gcdSplit)
    c = "y"
    while c == "y":
            
        for column in gcdSplit:
            print(f"Key {gcdSplit.index(column)} analysed: {column[0:150]}")
        
        print()
        print("English frequency: ", sorted(frequencyEng.items(), key= lambda x:(x[1]), reverse=True), "\n")
        mostCommonLetter = analyseColumns(gcdSplit)
        
        a = input("SwapUnderscore / PrintCipher / SwapSingel / bruteKey / End? (u / p / s / k / e): ")
        print()
        if a == "u":
            for i in range(len(gcdSplit)):
                gcdSplit[i] = gcdSplit[i].replace(mostCommonLetter[i], "|")
                history[i] +=  (f"{mostCommonLetter[i]} -> |, ")
        elif a == "p":
            for i in range(len(gcdSplit[0])):
                for j in range(len(gcdSplit)):
                    ciphMod += gcdSplit[j][i]
                    print(gcdSplit[j][i], end="")
            print()
        elif a == "s":
            col = int(input("Enter column number to swap letters: "))
            print(f"Histogram of column:  {history[col]}:", "\n\n")
            x,y = input("Enter letters to swap X -> y: ").split()
            if x != y:
                gcdSplit[col] = gcdSplit[col].replace(x, y)
                history[col] +=  (f"{x} -> {y}, ")
        elif a == "k":
            ciph, plain = input(f"Enter cipher and possible plain of length {gcd}: ").split()
            key = keyBruteVigenere(ciph, plain)
            plainText = decryptVigenere(cipher, key)
            if plainText != "":
                return plainText
        elif a == "e":
            c = "n"
            return plainText
        
        print()
        

# Brute force key by comparing cipher and plain text      
def keyBruteVigenere(cipher, plain):
     
    key = ""
    for i in range(len(cipher)):
        key += alphabet[(alphabet.index(cipher[i]) - alphabet.index(plain[i]))%len(alphabet)]
    print("Possible Key: ", key, "\n")
    
    return key       
    
# Decrypt cipher with key
def decryptVigenere(cipher, key):
    
    plain = ""
    for i in range(len(cipher)):
        plain += alphabet[(alphabet.index(cipher[i]) - alphabet.index(key[i%len(key)]))%len(alphabet)]
    
    print("Possible Plain: ", plain[0:500], "\n")
    i = input("Correct decryption? (y/n): ")
    print()
    if i == "y":
        return plain.replace("_", " ").replace("#", "\n")
    else:
        return ""



# Hardcoded solution once key is found
def decryptSubstition(cipher):
   
    for set in solution1:
        cipher = cipher.replace(set[0], set[1])

    return cipher.replace("|", " ").replace("#", "\n").upper()
    
# Main function to read input file and to write output to file

def decryptCeasar(cipher, shift):
    
    plain = ""
    for i in range(len(cipher)):
        plain += alphabet[(alphabet.index(cipher[i]) - shift)%len(alphabet)]
    
    return plain.replace("_", " ").replace("#", "\n").upper()



def main():

    cipherText = ""
    finalCipher = ""
    
    inputFile = input("Enter crypto file to decrypt: ")
    with open(inputFile, "r", encoding='UTF-8') as file:
        for line in file:
            if line[-1] == '\n':
                cipherText += line[:-1]
            else:
                cipherText += line
    file.close()        
    
    cipherType = input("Ceasar / Substitution / Vigenere / HardcodedSolution? (c / s / v / h): ")
    
    if cipherType == "c":
        shift = bruteCeasar(cipherText[0:70])
        finalCipher = decryptCeasar(cipherText, shift)
    elif cipherType == "s":
        mostCommon = analyseLetters(cipherText)
        swappedCipher, readWords = analyseSubstitution(cipherText, mostCommon)
        finalCipher = swapLetter (swappedCipher, readWords)
    elif cipherType == "v":
        gcd = vigenereAnalyse(cipherText)
        finalCipher =vigenereCrack(cipherText, gcd)
    elif cipherType == "h":
        finalCipher = decryptSubstition(cipherText)
    
   
    print(finalCipher)
    wrt = input("Write to file? (y/n): ")
    if wrt == "y":
        name = input("Enter filename: ")
        with open(name, "w") as outfile:
            outfile.writelines(finalCipher)
            outfile.close()



if __name__ == "__main__":
    main()