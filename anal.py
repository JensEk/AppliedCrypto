#!/usr/bin/env python3

alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#"     # 38 characters in total


# frequency analysis
def analyse(readLetters):
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

def bruteSubstitution(cipher, topletters):
    
    swapFirst = cipher.replace(topletters[0][0], "'_'").replace(topletters[1][0], "'e'")
    swapSecond = cipher.replace(topletters[0][0], "'e'").replace(topletters[1][0], "'_'")
    print(f"Bruteforcing substitution cipher: {cipher}")
    print(f"Substituted {topletters[0][0]} with _ and {topletters[1][0]} with e : {swapFirst}")
    print(f"Substituted {topletters[0][0]} with e and {topletters[1][0]} with _ : {swapSecond}")
    
    
    

def main():
    readLetters = {}
    cipherText = ""
    
    with open("ctext1.txt", "r", encoding='UTF-8') as file:
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
            
    mostCommon = analyse(readLetters)
    bruteCeasar(cipherText[0:70])
    bruteSubstitution(cipherText[0:100], mostCommon)





if __name__ == "__main__":
    main()