import math

import numpy as np
import os


# Main driver
def get_recommendation(word_list, color_patterns):
    if len(word_list) == 1:
        return word_list[0]

    curr_word = word_list[0]
    curr_max_entropy = 0
    for guess_word in word_list:
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


def generate_all_permutations_of_colours(length_of_word):
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
                new_s += "B"
            elif j == '1':
                new_s += "Y"
            elif j == '0':
                new_s += "G"
        A[index] = new_s
    return A


# Returns the filtered search space after a guess is made
def get_redefined_word_list(guess_word, colours, possible_words):
    indexes_of_black = []
    indexes_of_green = []
    indexes_of_yellow = []

    black_characters = []
    green_characters = []
    yellow_characters = []

    for i in range(len(colours)):
        if colours[i] == 'B':
            indexes_of_black.append(i)
            black_characters.append(guess_word[i])
        elif colours[i] == 'G':
            indexes_of_green.append(i)
            green_characters.append(guess_word[i])
        elif colours[i] == "Y":
            indexes_of_yellow.append(i)
            yellow_characters.append(guess_word[i])

    # filtered_green = np.array(possible_words).reshape(-1, )

    # for i in range(len(green_characters)):
    #     green_character = green_characters[i]
    #     index_of_green = indexes_of_green[i]
    #     filtered_green = np.where(filtered_green[index_of_green] == green_character, 1, 0)

    green_arr = [1 for i in range(len(possible_words))]
    for count in range(len(possible_words)):
        for i in range(len(green_characters)):
            single_word = possible_words[count]
            green_character = green_characters[i]
            index_of_green = indexes_of_green[i]
            if single_word[index_of_green] != green_character:
                green_arr[count] = 0
                break

    new_possible_words2 = []
    for i in range(len(possible_words)):
        if green_arr[i] == 1:
            new_possible_words2.append(possible_words[i])

    yellow_arr = [1 for i in range(len(new_possible_words2))]
    for count in range(len(new_possible_words2)):
        for i in range(len(yellow_characters)):
            single_word = new_possible_words2[count]
            yellow_character = yellow_characters[i]
            index_of_yellow = indexes_of_yellow[i]
            # If single_word contains a yellow char in its exact index
            if single_word[index_of_yellow] == yellow_character:
                yellow_arr[count] = 0
                break

            count_of_char_in_single_word = 0
            count_of_char_in_yellow_characters = 0
            for j in range(len(single_word)):
                if j not in indexes_of_green and single_word[j] == yellow_character:
                    count_of_char_in_single_word += 1
            for j in yellow_characters:
                if j == yellow_character:
                    count_of_char_in_yellow_characters += 1
            if count_of_char_in_single_word < count_of_char_in_yellow_characters:
                yellow_arr[count] = 0
                break

    new_possible_words3 = []
    for i in range(len(new_possible_words2)):
        if yellow_arr[i] == 1:
            new_possible_words3.append(new_possible_words2[i])
    # new_possible_words3 = new_possible_words2.copy() OLD ONE

    black_arr = [1 for i in range(len(new_possible_words3))]
    for count in range(len(new_possible_words3)):
        for i in range(len(black_characters)):
            single_word = new_possible_words3[count]
            black_character = black_characters[i]
            index_of_black = indexes_of_black[i]
            # If single_word contains a black char in its exact index
            if single_word[index_of_black] == black_character:
                black_arr[count] = 0
                break
            count_of_char_in_green_and_yellow = 0
            count_of_char_in_single_word = 0
            for j in green_characters:
                if j == black_character:
                    count_of_char_in_green_and_yellow += 1
            for j in yellow_characters:
                if j == black_character:
                    count_of_char_in_green_and_yellow += 1
            for j in single_word:
                if j == black_character:
                    count_of_char_in_single_word += 1
            if count_of_char_in_single_word > count_of_char_in_green_and_yellow:
                black_arr[count] = 0
                break
    new_possible_words4 = []
    for i in range(len(new_possible_words3)):
        if black_arr[i] == 1:
            new_possible_words4.append(new_possible_words3[i])

    return new_possible_words4


def solver():
    dir_path = os.getcwd()
    # os.path.join(dir_path, 'words.txt') is equivalent to dir_path + '\words.txt'
    word_list = open(os.path.join(dir_path, 'words.txt'), 'r').read().splitlines()
    possible_color_patterns = generate_all_permutations_of_colours(5)

    word_to_be_guessed = "tares"
    print("WordleSolver suggests you enter: {word}".format(word=word_to_be_guessed))
    word_guessed = input('Enter the word you guessed in non-caps: ')
    color_outcome = input('Enter the color outcome of your guess in caps: ')
    if color_outcome == 'GGGGG':
        return True
    word_list = get_redefined_word_list(word_guessed, color_outcome, word_list)

    while len(word_list) != 0:
        word_to_be_guessed = get_recommendation(word_list, possible_color_patterns)
        print("WordleSolver suggests you enter: {word}".format(word=word_to_be_guessed))
        word_guessed = input('Enter the word you guessed in non-caps: ')
        color_outcome = input('Enter the color outcome of your guess in caps: ')
        if color_outcome == 'GGGGG':
            return True
        word_list = get_redefined_word_list(word_guessed, color_outcome, word_list)


solver()
