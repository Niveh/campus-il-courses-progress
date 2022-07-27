import os
import time


def clear():
    os.system("cls")


logo = ''' 
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/    
                   '''

HANGMAN_PHOTOS = {
    1: """
    x-------x

    """,
    2: """
    x-------x
    |
    |
    |
    |
    |

    """,
    3: """
    x-------x
    |       |
    |       0
    |
    |
    |

    """,
    4: """
    x-------x
    |       |
    |       0
    |       |
    |
    |

    """,
    5: """
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |

    """,
    6: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |

    """,
    7: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |

    """
}


# print the main game logo
def print_hangman_logo():
    clear()
    print(logo)


# print the hangman based on number of tries
def print_hangman_tries(num_of_tries):
    print(HANGMAN_PHOTOS[num_of_tries])


# check if the secret word has been guessed
def check_win(secret_word, old_letters_guessed):
    win = True
    for i in secret_word:
        if i not in old_letters_guessed:
            win = False
            break
    return win


# show the guessed letters of the secret word
def show_hidden_word(secret_word, old_letters_guessed):
    final = []
    for i in secret_word:
        if i in old_letters_guessed:
            final.append(i)
        else:
            final.append("_")
    return " ".join(final)


# check if guessed letter is valid -- ended up not having to use it
def check_valid_input(letter_guessed, old_letters_guessed):
    letter_guessed = letter_guessed.lower()
    if len(letter_guessed) != 1 or not letter_guessed.isalpha() or letter_guessed in old_letters_guessed:
        return False
    return True


# check if the guessed letter is valid and update the old_letters_guessed list
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    letter_guessed = letter_guessed.lower()
    if len(letter_guessed) == 1 and letter_guessed.isalpha():
        if letter_guessed not in old_letters_guessed:
            old_letters_guessed.append(letter_guessed)
            return True
    print("That letter has already been guessed!\n")
    return False


# choose a word from a text file based on user's index
def choose_word(file_path, index):
    with open(file_path, "r") as f:
        words = f.read().strip().split(" ")

        return words[(index - 1) % len(words)]


# check if the user would like to play again
def play_again():
    return input("What shall we do next?\nType 'yes' to play again or anything else to quit: ").strip().lower() == 'yes'


# game logic function, has the ability to run recursively
def run_hangman_game(MAX_TRIES=6):
    print_hangman_logo()

    # set up everything we need for a fresh game
    file_path = input("Enter file path: ")
    word_index = int(input("Enter word index: "))
    secret_word = choose_word(file_path, word_index)
    old_letters_guessed = []
    num_of_tries = 0

    # creates anticipation :)
    print("Starting game in 3, 2, 1...")
    time.sleep(3)

    while num_of_tries <= MAX_TRIES:
        if check_win(secret_word, old_letters_guessed):
            break

        # visual improvements
        # clear the console and show the hangman logo and art each round
        clear()
        print_hangman_logo()
        print_hangman_tries(num_of_tries + 1)

        print(show_hidden_word(secret_word, old_letters_guessed) + "\n")

        # always show the guessed letters, it's much more convenient
        if len(old_letters_guessed) > 0:
            print("\nPreviously guessed letters:\n" +
                  " -> ".join(sorted(old_letters_guessed)) + "\n")

        # make sure we show the final hangman art without playing an extra
        if num_of_tries == MAX_TRIES:
            break

        guess = input("Guess a letter: ")
        while not try_update_letter_guessed(guess, old_letters_guessed):
            guess = input("Guess a letter: ")

        if guess not in secret_word:
            num_of_tries += 1
            print("Incorrect Guess :(")

            # visual improvement
            time.sleep(2)

    # check if game ended due to win or loss
    if check_win(secret_word, old_letters_guessed):
        print("\nGood job! You've successfully guessed the word!")
    else:
        print("\nOh well, you win some and you lose some. Seems like you lost this time.")

    # play again by calling the main game function recursively (or not)
    if play_again():
        run_hangman_game()
    else:
        print("\nThank you for playing! I will close myself in 5 seconds :(")
        time.sleep(5)
        exit()


def main():
    run_hangman_game()


if __name__ == "__main__":
    main()
