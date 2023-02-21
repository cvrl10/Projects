import random

class Hangman:
    def __init__(self, tries=6, file='words.txt'):
        self.__tries = tries
        self.__li = []
        with open(file, 'r') as file:
            for word in file:
                self.__li.append(word if word[-1]!='\n' else word[:len(word)-1])
                
    def play(self):
        word = random.choice(self.__li)
        guess = list('_')*len(word)
        used_letters = ''
        tries = self.__tries
        
        while tries:
            print(f'You have {tries} tries left.' if tries>1 else 'You have 1 try left.')
            print('Used letters:', *used_letters)
            print('Word:', *guess)
            letter = input('Guess a letter: ').lower()
            
            if letter in used_letters:
                print()
                continue
            
            used_letters += letter
            tries += self.__updateguesslist(guess,letter,word)
            
            if ''.join(guess) == word:
                print(f'You guessed the word {word} !')
                return
            else:
                print()
                tries -= 1
        
        print(f'The word was {word}')
            
    def __updateguesslist(self, guess, letter, word):
        '''the integer that is return is to avoid decrementing tries if guess is correct'''
        i = word.find(letter)
        result = 1 if i!=-1 else 0
        while i!=-1:
            guess[i] = letter
            i = word.find(letter, i+1)
        return result
            
            
            
