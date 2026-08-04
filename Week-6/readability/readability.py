from cs50 import get_string

# return the number of letters in text
def count_letters(text):
    letters = 0
    for char in text:
        if char.isalpha():
            letters += 1
    return letters

# return the number of words in text
def count_words(text):
    words = 1
    for char in text:
        if char == " ":
            words += 1
    return words

# return the number of sentences in text
def count_sentences(text):
    sentences = 0
    for char in text:
        if char == "." or char == "!" or char == "?":
            sentences += 1
    return sentences


def main():
    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # compute the coleman-liau index
    L = (letters / words) * 100
    S = (sentences / words) * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    # print the grade level
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


main()
