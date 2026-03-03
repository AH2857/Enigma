from string import ascii_uppercase
abcStr          = ascii_uppercase + '_'        
print(abcStr)    
# index 26 of rotor string is the turnover position:
rotorTypes      = ['rotorI',    'EKMFLGDQVZNTOWYHXUSPAIBRCJR']
reflectorTypes  = ['reflectA',  'EJMZALYXVBWFCRQUONTSPIKHGD_']

# --------------------------------------------------------------------------------------------------------------------------------

def shiftIndex(letterIndexSI, ShiftSI):                             # Inputs: letterIndex, index shift distance
    letterIndexSI += ShiftSI                                        # Shift Index 
    if(letterIndexSI > 25):                                         # Rollover if over 25
        letterIndexSI += -26                                        # Minus 26, so brought back into range    
        # print('Index wrapped back around')      
    return letterIndexSI

def indexFinder(letterIF, strIF):                                   # find letter characters index in the given string (abcStr or RotorType)
    indexIF = 0                
    while letterIF != strIF[indexIF]:                               # check if letter at index matches letter            
        indexIF += 1                                                # if not, increment index
    return indexIF                                                  # return index when match is found

def rotorPass(letterIndexRP, rotorPosRP, rotorTypeRP, reverseRP):   # reverse: is signal passing through rotor forwards or backwards
    if reverseRP == 1:
        letter = abcStr[letterIndexRP]                              # convert letter index into encoded letter character
        letterIndexRP = indexFinder(letter, rotorTypeRP)            # set index to index of letter connected to that letter
    else:    
        letter = rotorTypeRP[letterIndexRP]                         # convert letter index into encoded letter character
        letterIndexRP = indexFinder(letter, abcStr)                 # set index to index of letter connected to that letter
    return letterIndexRP

def rotorSet(rotorKeyRS,rotorPositionsRS,noOfRotorsRS):             # set rotorPositions to key positions 
    i = 0
    while i < noOfRotorsRS:
        rotorPositionsRS[i]=indexFinder(rotorKeyRS[i], abcStr)      # set rotor position to rotor Key character
        #print(rotorPositionsRS)
        i += 1                                                      # increment rotor
    return rotorPositionsRS

def keyPressShift(rotorPositionsKPS,rotorsKPS):                     # key press shifting
    # shift for each key press:
    # "press" rotates the first rotor
    # and rotates the 2/3/4th rotor if they are on their turnover pos
    
    #print(rotorPositionsKPS[0])
    rotorPositionsKPS[0] = shiftIndex(rotorPositionsKPS[0],1)                   # increment rotor 0
    i = 1
    while i < len(rotorsKPS):                                                   # for each rotor position                                    
        if rotorPositionsKPS[i] == indexFinder(rotorsKPS[i][26],abcStr):        # if position of rotor is shift position
            rotorPositionsKPS[i] = shiftIndex(rotorPositionsKPS[i],1)           # increment rotor 123 if on turnover position (index 26 of rotor array)          
        i+=1
        #print(testRotorPositions)
    return rotorPositionsKPS

def reflectorPass(letterIndexRP, reflectorTypeRP):
    letter = reflectorTypeRP[0][letterIndexRP]                                  # convert letter index into encoded letter character
    letterIndexRP = indexFinder(letter, abcStr)                                 # set index to index of letter connected to that letter
    return letterIndexRP

def fullPass(numOfRotorsFP,LetterIndexFP,rotorPositionsFP,rotorsFP,reflectorFP):
    # 'key'->rtr1->rtr2->rtr3->refl->rtr3*->rtr2*->rtr1*->'light'
    f = -1
    while f < (numOfRotorsFP-1):
        f += 1
        LetterIndexFP = rotorPass(LetterIndexFP,rotorPositionsFP,rotorsFP[f],0)
    LetterIndexFP = reflectorPass(LetterIndexFP,reflectorFP)
    while f >= 0:
        LetterIndexFP = rotorPass(LetterIndexFP,rotorPositionsFP,rotorsFP[f],1)
        f -= 1
    return LetterIndexFP

def rotorKeyAssembler():            # sets up rotors (number/positions) after picking key 
    print('Enter Key:')             # prompt input in terminal: type rotorKey
    #rotorKey    = input()
    #rotorKey    = '0RED'               # dummy input for testing
    rotorKey     = 'ring'
    rotorPositionsRKA = []
   
    validKeyEntered = 0
    while validKeyEntered == 0:
        if  True != rotorKey.isalpha():         # if key not valid: (not an upper or lower case letter)
            print('Enter new Key, not valid:')  
            rotorKey = input()   
        else:                                   # if it is a valid character (letter):
            print('valid Key')
            validKeyEntered += 1

    indexRKA        = 0
    rotorKey        = rotorKey.upper()                              # convert letter to capital letter
    rotorsRKA       = []
    reflectorRKA    = []

    print(rotorTypes)
    while indexRKA < len(rotorKey):                                 # for each letter:
        letterIndexRKA = indexFinder(rotorKey[indexRKA], abcStr)    # convert letter of key into index
        rotorPositionsRKA.append(letterIndexRKA)                    # append index to starting rotor positions
        
        print('Select rotor', indexRKA+1, 'type')
        validRotorEntered = 0 
        #rotor = input()
        rotor = 'rotorI'    # test only
        while validRotorEntered == 0:
            if rotor in rotorTypes:                                 # check that input is a rotor type
                print('-> Rotor selected:',rotor)
                rotorsRKA.append(rotorTypes[rotorTypes.index(rotor) + 1])
                print('-> Rotor profile: ',rotorTypes[rotorTypes.index(rotor) + 1])
                validRotorEntered += 1
            else:
                print('Not a rotor type, Select a rotor')
                rotor = input()
        indexRKA += 1
    
    print('Select reflector type')
    print(reflectorTypes)
    #reflector = input()
    reflector = 'reflectA'  # test only
    validReflectorEntered = 0
    while validReflectorEntered != 1:
        if reflector in reflectorTypes:
            print('-> Reflector selected:',reflector)
            reflectorRKA.append(reflectorTypes[reflectorTypes.index(reflector) + 1])
            print('-> Reflector profile: ',reflectorTypes[reflectorTypes.index(reflector) + 1])
            validReflectorEntered += 1
        else:
            print('Not a reflector type, Select a reflector')
            reflector = input()

    #print(rotorPositionsRKA)
    #print(rotorsRKA)
    return rotorPositionsRKA, rotorsRKA, reflectorRKA

def textInputHandler(rotorPositionsTIH, rotorsTIH, reflectorTIH):
    print('Enter text to encrypt/decrypt:')

    text = input()

    #text = 'in the bleak midwinter. rabble3 r33ble5'  # test only

    #text = open("EnigmaTestText2.txt")                   # long test only
    #text = text.read()                                  # long test only
    # testing using text input from .txt is broken, reads the length of the string wrong OR the string is the wrong length. 

    textlength = len(text)
    print(textlength)
    text = text.upper()                                     # replace letters with capitals
    savedText = text                                        # save text
    
    indexTIH = 0
    while indexTIH < textlength:                                                                                # THEN for each character in string:
        #print(indexTIH)
        #if text[indexTIH].isalpha():                                                                            # check if letter 
        #if text[indexTIH].isascii():                                                                            # check if letter 
        if text[indexTIH].isalpha() and text[indexTIH].isascii():                                                # check if letter 
            #print('rotor positions before press', rotorPositions)
            rotorPositionsTIH = keyPressShift(rotorPositionsTIH, rotorsTIH)                                     # simulate key press, shift correct rotors 
            #print('rotor positions after press', rotorPositions)
            #print(text[indexTIH])
            letterindexTIH = indexFinder(text[indexTIH],abcStr)
            letterindexTIH = fullPass(len(rotorsTIH),letterindexTIH,rotorPositionsTIH,rotorsTIH,reflectorTIH)   # then replace letter in string with the encoded letter        
            text_list = list(text)                                                                              # convert from string to array of characters
            text_list[indexTIH] = abcStr[letterindexTIH]                                                        # editing character in list (cant edit in string)
            text = ''.join(text_list)                                                                           # add onto output string
        indexTIH += 1                                                                                           # increment along string

    # pass string through machine again to decrypt it, 
    # (checking the code worked or printing error)
    textTestDecrypt = text
    indexTIH = 0
    while indexTIH < textlength:                                                                                # THEN for each character in string:
        if textTestDecrypt[indexTIH].isalpha():                                                                 # check if letter 
            #print('rotor positions before press', rotorPositions)
            rotorPositionsTIH = keyPressShift(rotorPositionsTIH, rotorsTIH)                                     # simulate key press, shift correct rotors 
            #print('rotor positions after press', rotorPositions)
            letterindexTIH = indexFinder(textTestDecrypt[indexTIH],abcStr)
            letterindexTIH = fullPass(len(rotorsTIH),letterindexTIH,rotorPositionsTIH,rotorsTIH,reflectorTIH)   # then replace letter in string with the encoded letter
            text_list = list(textTestDecrypt)                                                                   # convert from string to array of characters
            text_list[indexTIH] = abcStr[letterindexTIH]                                                        # editing character in list (cant edit in string)
            textTestDecrypt = ''.join(text_list)                                                                # add onto output string
        indexTIH += 1                                                                                           # increment along string

    if textTestDecrypt == savedText:
        print('successful encrypt decrypt')
        #print('Test: De-encrypted text: 'textTestDecrypt)

    return text

# ----------------------------------------------------------------------------------------------------------------------------------------------

# tested up to _ characters input text:
# success 698, 1777, 1777, 1799, 1821, 
# fail 1834, 1834, 1834, 1834, 

## Main                                                    

rotorPositions,rotors,reflector = rotorKeyAssembler()       # pick key, and rotors and reflector
text = textInputHandler(rotorPositions, rotors, reflector)
print(text)                                                 # print encoded string with all non letter characters untouched

# give option to continue writing (adding to end)
# give option to restart and encrypt something else w/out restarting
