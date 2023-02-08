"""
file: spellfixer.py

description: this program spell fixes the words in a user input sentence
when it is provided with a words list file and a file containing adjacent keys

language: python3

author: Snehil Sharma (ss7696)
author: Koteswara Rao Bade (kb5608)
"""

import string


def load_keys(adjacent_keys: string):
    """
    this function reads a file and
    makes a dictionary that stores
    the adjacent keys for each key
    
    """
    
    
    with open( adjacent_keys ) as key_read:

        for line_number in key_read:
            #remove white spaces
            current_line = line_number.strip()
            #split based on spaces
            data = current_line.split(' ')
            #the first element in the line is the key
            the_key = data[ 0 ]
            #the rest of the elements are adjacent keys
            keys[the_key] = data[ 1 : ]


def valid_word( word_to_check: string )->bool:
    """
    this function accesses a words list file
    and finds if the input string has a match 
    in the file
    """
    
    if len(word_to_check) == 1:
        #return true if the word length is 1
        return True

    #open words file
    with open(word_doc ) as words:
        
        for the_words in words:
            
            #strip white spaces
            current_word = the_words.strip()

            
            if current_word != "" :
                #if word exists in file
                if word_to_check == current_word:

                    return True


def adjacent_hit(input_word: string)->string:
    """
    this function tries to spellfix a word that 
    might have been misspelled by hitting a key
    that is adjacent to the intended key
    """
    #split the input word into list of letters
    letter_list = list(input_word)

    #traverse the letters
    for i in range(len(letter_list)):
            
            #store the adjacent keys of current letter
            checker =  keys.get( letter_list[i] )
        
            #traverse the adjacent keys
            for j in range(len(checker)):

                #temporary list that stores the letters
                temp = list(input_word)
                #delete the current letter
                del temp[i]
                
                #insert the current adjacent key
                temp.insert( i, checker[ j ] )
                
                #convert list back to word
                word_to_check = ''.join(temp)

                #check if the word exists
                if valid_word(word_to_check):
                    #return the word if found
                    return word_to_check

    #return the input word without changes if no matches found                
    return input_word
    


def swap_letters(input_word: string)->string:
    """
    this function spellfixes words that might
    be misspelled due to two letters being swapped
    """

    letter_list = list(input_word)
    
    #traverse the letters
    for i in range(len(letter_list)):
        
        #re-initialize list of letters 
        to_swap = list(input_word)

        #if index of next letter is not out of bounds
        if ( i+1 < len(to_swap) ):

            #store the next letter
            var_one = to_swap[i+1]

            #delete the next letter from list
            del to_swap[i+1]
            
            #insert that letter at the index of the current letter, thus swapping their positions
            to_swap.insert(i, var_one)
            
            #convert back to a word
            word_to_check = ''.join(to_swap)

            #check if the word exists
            if valid_word(word_to_check):

                #return the word if found
                return word_to_check

    #return the input word without changes if no matches found
    return input_word


def delete_letter(input_word: string)->string:
    """
    this function spellfixes a word that might
    be misspelled due to an extra letter in the word
    """
    letter_list = list(input_word)

    #traverse the letters
    for i in range( len( letter_list ) ):

        #re-initialize list of letters
        to_delete = list( input_word )

        #delete the current letter
        del to_delete[i]

        #convert back to word
        word_to_check = ''.join(to_delete)

        #check if the word exists    
        if valid_word(word_to_check):
            #return the word if found
            return word_to_check

    #return the input word without changes if no matches found
    return input_word

         

def spell_check( input_word: string ) -> set:
    """
    this function function passes misspelled word to
    to functions that try to spellfix that word and then
    returns a set of fixes for that word
    """
    
    letter_list = list(input_word)

    #initialize the set
    suggested_words = set()

    
    if valid_word(input_word):
        #return the input word if the word is not misspelled
        return input_word
    
    #if the set is empty
    elif(suggested_words == set()):

        #get the spellfix for adjacent key hit misspell
        check = adjacent_hit( input_word )

        #add the spellfix to the set
        suggested_words.add( check )

        #if the adjacent hit returned the input word, meaning mispell was not due to adjacent hit
        if input_word in suggested_words:

            #reinitialize the set
            suggested_words = set()

            #get the spellfix if the letters were swapped
            check = swap_letters( input_word )

            #add the word to the set
            suggested_words.add( check )
            
            #if swap letters returned the input word, meaning mispell was not due to swap letters
            if input_word in suggested_words:

                #reinitialize the set
                suggested_words = set()

                #get the spellfix if there was extra letter
                check = delete_letter( input_word )
             
                ##add the word to the set
                suggested_words.add( check )

        #return the suggested words set       
        return suggested_words


if __name__ == "__main__":

    #initialize the adjacent keys dictionary
    keys = dict()

    #input the file names
    word_doc = input("Enter the name of words file: ")
    keyboard_file = input("Enter name of keyboard file: ")
    
    #print usage and exit if the file names are wrong
    if (keyboard_file != "keyboard.txt") or (word_doc != "words.txt") :
        print("Usage: python3 spellfixer.py words- words.txt keyboard- keyboard.txt")
        exit(0)

    #make the adjacent keys dictionary
    load_keys(keyboard_file)

    print("Type '!*!' to terminate")
    #initialize the string user_input
    user_input = ""

    #run loop until the user inputs !*!
    while(("!*!" in user_input) ==  False):

        #take user input
        user_input = str(input("Enter your sentence: "))

        #as long as input is not !*!
        if user_input != "!*!" :

            #strip white spaces from input
            stripped_input = user_input.strip()

            #extract words from sentence and put into list
            words_extracted = stripped_input.split(" ")

            #traverse the words
            for j in range(len(words_extracted)):

                #make a temporary copy of the list of words extracted
                temp_list = words_extracted

                #get the spellfix for the current word
                suggestion = spell_check(temp_list[j])

                #if the same word is returned
                if temp_list[j] in suggestion:
                    #empty the set
                    suggestion = set()

                #if suggestions is not empty set
                if suggestion != set() :
                    
                    #delete the current word from the list
                    del temp_list[j]

                    #get the spellfixed word
                    x = suggestion.pop()

                    #insert the spellfixed word back into list
                    temp_list.insert(j, x )

                    #convert back to sentence        
                    fixed = ' '.join(temp_list)

                    #print the sentence with the spellfixed word
                    print("Spell fixed sentence: " + fixed)
        else:

            #terminate if the user input was !*!
            print("Bye!")
            exit(0)


    


