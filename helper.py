def get_green_indexes_and_characters_of_guess_word(guess_word, colors):
    green_indexes = []
    green_characters = []

    for i in range(len(colors)):
        if colors[i] == 'g':
            green_indexes.append(i)
            green_characters.append(guess_word[i])
    return green_indexes, green_characters


def get_yellow_indexes_and_characters_of_guess_word(guess_word, colors):
    yellow_indexes = []
    yellow_characters = []

    for i in range(len(colors)):
        if colors[i] == 'y':
            yellow_indexes.append(i)
            yellow_characters.append(guess_word[i])
    return yellow_indexes, yellow_characters


def get_black_indexes_and_characters_of_guess_word(guess_word, colors):
    black_indexes = []
    black_characters = []

    for i in range(len(colors)):
        if colors[i] == 'b':
            black_indexes.append(i)
            black_characters.append(guess_word[i])
    return black_indexes, black_characters


def filter_word_list_by_green(possible_words, green_indexes, green_characters):
    green_arr = [1 for i in range(len(possible_words))]

    for i in range(len(possible_words)):
        single_word = possible_words[i]
        for j in range(len(green_indexes)):
            green_character = green_characters[j]
            index_of_green = green_indexes[j]
            # If single_word does not contain the green char in its exact index
            if single_word[index_of_green] != green_character:
                green_arr[i] = 0
                break

    filtered_possible_words = []
    for i in range(len(possible_words)):
        if green_arr[i] == 1:
            filtered_possible_words.append(possible_words[i])
    return filtered_possible_words


def filter_word_list_by_yellow(possible_words, green_indexes, yellow_indexes, yellow_characters):
    yellow_arr = [1 for i in range(len(possible_words))]

    for count in range(len(possible_words)):
        single_word = possible_words[count]
        for i in range(len(yellow_characters)):
            yellow_character = yellow_characters[i]
            index_of_yellow = yellow_indexes[i]
            # If single_word contains a yellow char in its exact index
            if single_word[index_of_yellow] == yellow_character:
                yellow_arr[count] = 0
                break

            count_of_char_in_single_word = 0
            count_of_char_in_yellow_characters = 0
            for j in range(len(single_word)):
                if j not in green_indexes and single_word[j] == yellow_character:
                    count_of_char_in_single_word += 1
            for j in yellow_characters:
                if j == yellow_character:
                    count_of_char_in_yellow_characters += 1
            # If single_word contains lesser of a certain yellow character than required
            if count_of_char_in_single_word < count_of_char_in_yellow_characters:
                yellow_arr[count] = 0
                break

    filtered_possible_words = []
    for i in range(len(possible_words)):
        if yellow_arr[i] == 1:
            filtered_possible_words.append(possible_words[i])
    return filtered_possible_words


def filter_word_list_by_black(possible_words, green_characters, yellow_characters, black_indexes, black_characters):
    black_arr = [1 for i in range(len(possible_words))]

    for count in range(len(possible_words)):
        single_word = possible_words[count]
        for i in range(len(black_characters)):
            black_character = black_characters[i]
            index_of_black = black_indexes[i]
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
            # A black character is black precisely because it is not inside the correct word. Thus, if single_word
            # contains more of a black character than allowed (ie green + yellow), then it is not an eligible guess.
            if count_of_char_in_single_word > count_of_char_in_green_and_yellow:
                black_arr[count] = 0
                break

    filtered_possible_words = []
    for i in range(len(possible_words)):
        if black_arr[i] == 1:
            filtered_possible_words.append(possible_words[i])
    return filtered_possible_words
