import json

def load_words():
    with open('path/to/words_dictionary.json') as word_file:
        valid_words = json.load(word_file)

    return valid_words

def has_repeating_letters(word):
    return len(word) != len(set(word))

def get_five_letter_words(word_array, include_words_with_repeating_letters):
    if include_words_with_repeating_letters:
        return {word for word in word_array if len(word) == 5}
    else:
        return {word for word in word_array if len(word) == 5 and not has_repeating_letters(word)}

def words_without_main_vowels(word_array):
    mainline_vowels = "aeiou"
    return {word for word in word_array if not any(set(word) & set(mainline_vowels))}

def words_not_containing_letters(word_array, letter_string):
    return {word for word in word_array if not any(set(word) & set(letter_string))}

def words_containing_letters(word_array, letter_string):
    return {word for word in word_array if all(c in word for c in set(letter_string))}

def get_potential_words(word_array, input, potential_letters, not_containing):
    potentials = []

    for word in word_array:
        if (len(word) == len(input) and all((c1 == "_") or (c1 == c2) for c1, c2 in zip(input, word))): # Check for words with confirmed letters in positions
            potentials.append(word)

    if len(potential_letters) > 0:
        potentials = words_containing_letters(potentials, potential_letters) # Make sure the potential words contain the orange letters

    if len(not_containing) > 0:
        potentials = words_not_containing_letters(potentials, not_containing) # Remove any words that contain gray letters

    return potentials

if __name__ == '__main__':
    # So far, I haven't seen Wordle use a word with repeating letters.
    # In any case, let this be a variable in case that changes in the future.
    INCLUDE_WORDS_WITH_REPEATING_LETTERS = False

    solved = False
    was_solved = ""

    print("Wordle!!")

    english_words = load_words()
    potential_words = get_five_letter_words(english_words, INCLUDE_WORDS_WITH_REPEATING_LETTERS)
    words_without_aeiou = words_without_main_vowels(potential_words)
    possible_words_after_two_rounds_of_wordle = words_not_containing_letters(words_without_aeiou, "tnscl")

    while not solved:
        init_input = input("Enter a word for potential matches. Use \"_\" to signify GRAY or ORANGE letters: ")
        potential_letters = input("Enter ORANGE colored letters: ")
        not_containing = input("Enter GRAY colored letters: ")

        potential_words = get_potential_words(potential_words, init_input.lower(), potential_letters.lower(), not_containing.lower())

        potential_word_string = ", ".join(potential_words)
        print(f"Potential Words: {potential_word_string}")

        was_solved = input("Did you solve it? (yes/y/no/n): ")

        while "n" not in was_solved.lower() and "y" not in was_solved.lower():
            was_solved = input("Did you solve it? (yes/y/no/n): ")

        if "y" in was_solved.lower(): 
            solved = True

    print("Great job!")
