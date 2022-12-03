import math
import numpy as np
import os
from constant import LENGTH_OF_WORD
from helper import get_green_indexes_and_characters_of_guess_word, get_yellow_indexes_and_characters_of_guess_word, \
    get_black_indexes_and_characters_of_guess_word, filter_word_list_by_green, filter_word_list_by_yellow, \
    filter_word_list_by_black


# Returns the word with the highest entropy, ie the word that is most likely to reduce the search space maximally
def get_recommendation(word_list, initial_word_list, color_patterns):
    if len(word_list) == 1:
        return word_list[0]

    curr_word = word_list[0]
    curr_max_entropy = 0
    for guess_word in word_list:  # For exploration, word_list should be initial_word_list
        entropy_of_guess_word = calculate_entropy_for_a_guess_word(guess_word, word_list, color_patterns)
        if entropy_of_guess_word > curr_max_entropy:
            curr_word = guess_word
            curr_max_entropy = entropy_of_guess_word
    return curr_word


# Calculates entropy for a single guess word
def calculate_entropy_for_a_guess_word(word, word_list, color_patterns):
    curr_entropy = 0
    for color_pattern in color_patterns:
        p = len(get_redefined_word_list(word, color_pattern, word_list)) / len(word_list)
        if p == 0:
            continue
        i = math.log2(1 / p)
        curr_entropy += p * i
    return curr_entropy


# Returns a list of strings containing all possible colour patterns
def generate_all_permutations_of_colors(length_of_word):
    A = []
    n = 0
    multiplier = 1
    for i in range(length_of_word):
        n += 2 * multiplier
        multiplier *= 3

    while n > -1:
        num = np.base_repr(n, base=3)
        while len(num) < length_of_word:
            s = '0' + num
            num = s
        A.append(num)
        n -= 1
    for index in range(len(A)):
        new_s = ""
        for j in A[index]:
            if j == '2':
                new_s += "b"
            elif j == '1':
                new_s += "y"
            elif j == '0':
                new_s += "g"
        A[index] = new_s
    return A


# Returns the filtered search space after a guess is made
def get_redefined_word_list(guess_word, colors, possible_words):
    # Get the indexes and characters of guess_word by color
    green_indexes, green_characters = get_green_indexes_and_characters_of_guess_word(guess_word, colors)
    yellow_indexes, yellow_characters = get_yellow_indexes_and_characters_of_guess_word(guess_word, colors)
    black_indexes, black_characters = get_black_indexes_and_characters_of_guess_word(guess_word, colors)

    # Perform three rounds of filtering, one for each color
    word_list_after_filtering_green = filter_word_list_by_green(possible_words, green_indexes, green_characters)
    word_list_after_filtering_green_and_yellow = filter_word_list_by_yellow(word_list_after_filtering_green,
                                                                            green_indexes,
                                                                            yellow_indexes,
                                                                            yellow_characters)
    word_list_after_filtering_green_and_yellow_and_black = filter_word_list_by_black(
        word_list_after_filtering_green_and_yellow,
        green_characters,
        yellow_characters,
        black_indexes,
        black_characters)

    return word_list_after_filtering_green_and_yellow_and_black


# Main driver
def solver():
    dir_path = os.getcwd()
    # os.path.join(dir_path, 'words.txt') is equivalent to dir_path + '\words.txt'
    word_list = open(os.path.join(dir_path, 'words.txt'), 'r').read().splitlines()
    initial_word_list = open(os.path.join(dir_path, 'words.txt'), 'r').read().splitlines()
    possible_color_patterns = generate_all_permutations_of_colors(LENGTH_OF_WORD)

    num_of_guesses = 0
    # tares is the best known initial word to cut down the search space
    word_to_be_guessed = "tares"
    print(f"WordleSolver suggests you enter: {word_to_be_guessed}")
    word_guessed = input("Enter the word you guessed: ").lower()
    num_of_guesses += 1
    color_outcome = input("Enter the color outcome of your guess: ").lower()
    if color_outcome == 'ggggg':
        print(f"Congratulations! You took {num_of_guesses} guesses.")
        return
    word_list = get_redefined_word_list(word_guessed, color_outcome, word_list)
    print(f"Number of possible words left: {len(word_list)}")

    while len(word_list) != 0:
        word_to_be_guessed = get_recommendation(word_list, initial_word_list, possible_color_patterns)
        print(f"WordleSolver suggests you enter: {word_to_be_guessed}")
        word_guessed = input("Enter the word you guessed: ")
        num_of_guesses += 1
        color_outcome = input("Enter the color outcome of your guess: ")
        if color_outcome == 'ggggg':
            print(f"Congratulations! You took {num_of_guesses} guesses.")
            return
        word_list = get_redefined_word_list(word_guessed, color_outcome, word_list)

    # Invalid scenario
    print("You have encountered an erroneous scenario, ensure that you do not mistype.")


solver()
