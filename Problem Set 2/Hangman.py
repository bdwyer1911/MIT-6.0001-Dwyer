# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guessCheck = False
    for letter in secret_word:
        if letter in letters_guessed:
            guessCheck = True
        else:
            guessCheck = False
            break
    return guessCheck
    
def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    blanks = []
    for i in range(len(secret_word)):
        blanks.append('_')
    for letter in letters_guessed:
        if letter in secret_word:
            for i in range(len(secret_word)):
                if letter == secret_word[i]:
                    blanks[i] = letter
            
    return ' '.join(blanks)

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    allLetters = string.ascii_lowercase
    listLetters = list(allLetters)
    for letter in letters_guessed:
        if letter in allLetters:
            listLetters.remove(letter)
    return "".join(listLetters)
            

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Initialize some things
    guesses_remaining = 6 #initialize the number of guesses
    warnings_remaining = 3
    letters_guessed = [] #empty list to fill with the letters they guess
    vowels = 'aeiou' #keep track of vowels that will count as two guesses
    
    #print some opening statement
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is ' + str(len(secret_word)) + ' letters long.')
    print('--------------')
    
    #Code to run until word is guessed or we run out of guesses
    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:
        print('You have ' + str(guesses_remaining) + ' guesses left')
        print('You have ' + str(warnings_remaining) + ' warnings left')
        print('Available letters: ' + get_available_letters(letters_guessed))
        guess = input('Please guess a letter:').lower() #use .lower to make it lower case
        
        # #failsafe
        # if guess == 'abc':
        #     break
        
        #check if valid guess
        if guess not in string.ascii_lowercase or guess in letters_guessed:
            warnings_remaining -= 1
            
            #if they're out of warnings, it counts as a guess
            if warnings_remaining < 1:
                guesses_remaining -= 1
                warnings_remaining = 0
            
            #make sure they guess a letter
            if guess not in string.ascii_lowercase:
                print('Oops! That is not a valid letter. You have ' + str(warnings_remaining) + ' warnings left')
                print('--------------')
            
            #make sure they haven't already guessed the input
            if guess in letters_guessed:
                print('Oops! You already guessed that letter. You have ' + str(warnings_remaining) + ' warnings left')
                print('--------------')
                
        #proceed here if the guess is valid
        if guess not in letters_guessed and guess in string.ascii_lowercase:
            letters_guessed.append(guess) #add their guess to the list of guesses
            
            #if it's a good guess
            if guess in secret_word:
                print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
                print('--------------')
            
            #bad guess and a vowel counts as two guesses
            elif guess in vowels:
                print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
                print('--------------')
                guesses_remaining -= 2
            
            #bad guess and a consonant counts as one guess
            else:
                print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
                print('--------------')
                guesses_remaining -= 1
                
    #if they win, give thme a message and show score       
    if is_word_guessed(secret_word, letters_guessed):
        print('Congratulations, you won!')
        score = guesses_remaining * len(set(secret_word)) #used a set here as it doesn't allow duplicates, so it's an easy way to get the number of unique letters
        print('Your total score for this game is: ' + str(score))
    
    #LOSER!
    else:
        print("Sorry, but you're out of guesses. The word is " + secret_word)




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
