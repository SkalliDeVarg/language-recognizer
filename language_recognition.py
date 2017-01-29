import random
from lneurons_class import LNeurons
from wordbooks import wordbooks_ask
from wordbooks import convert_word

# For initialization all parameters are prompted.
print("Welcome to Leif's neuron based language recognizer with dynamically "
      "stacked pattern size. Everything should be quite self explanatory. "
      "Use 0 for unlimitied values. The bigger \"maxpattern\" is, the more"
      " accurate and memory consuming the process will be.")

maxpattern = int(input("Maximum pattern length: "))
minlength = int(input("Minimum length of words: "))
maxlength = int(input("Maximum length of words: "))
while True:
    convert = input("Convert Words to A-Z format? (y/n): ")
    if convert in ["y", "Y", "yes", "Yes"]:
        convert = True
        break
    elif convert in ["n", "N", "no", "No"]:
        convert = False
        break
word_count = int(input("How many languages to learn: "))
lang_list = []
for i in range(word_count):
    lang_list.append(input("Name of language file: "))
lang_count = len(lang_list)
wb = wordbooks_ask(minlength, maxlength, lang_list, convert)
brain = LNeurons(lang_list, maxpattern)

lifesign = 10000


def train(length):
    """
    This function calls the brain.train() function n times and prints
    progress all lifesign calls.
    """
    for i in range(1, length + 1):
        chosen_lang = random.choice(list(range(lang_count)))
        chosen_word = random.choice(wb[chosen_lang])
        brain.train(chosen_word, chosen_lang)
        if i % lifesign == 0 or i == length:
            print(str(i / length * 100) + "% done")


def test(length):
    """
    This function calls the brain.test() function n times, checks if the
    neurons choices are right or not, saves the results in two arrays, prints
    the total success rate all lifesign calls and at the end prints the success
    rates for all languages and total.
    """
    success_list = []
    indiv_success = [[] for i in range(lang_count)]
    for i in range(1, length + 1):
        right_lang = random.choice(list(range(lang_count)))
        chosen_word = random.choice(wb[right_lang])
        # The validity of the chosen language of the neurons is evaluated and
        # saved in two seperate arrays.
        attempt = brain.test(chosen_word)
        chosen_lang = attempt.index(max(attempt))
        if chosen_lang == right_lang:
            choice = 1
        else:
            choice = 0

        success_list.append(choice)
        indiv_success[right_lang].append(choice)
        if i % lifesign == 0 or i == length:
            print("Progress: "
                  + str(i / length * 100) + "%    "
                  + "Total success: "
                  + str(sum(success_list) / len(success_list) * 100)
                  + "%")
    print("")
    for i in range(lang_count):
        # This prevents division by zero.
        if len(indiv_success[i]) > 0:
            print(lang_list[i] + " success: "
                  + str(sum(indiv_success[i]) / len(indiv_success[i]) * 100)
                  + "%")
        else:
            print(lang_list[i] + " no sufficient data")
    print("")
    print("Total success: "
          + str(sum(success_list) / len(success_list) * 100)
          + "%")
    print("")
    input("Press ENTER to continue")


def ask(word):
    print("")
    # Prevents calling of convert with empty string.
    if word != "":
        chosen_word = convert_word(0, 0, word, convert)
    else:
        right_lang = random.choice(list(range(lang_count)))
        chosen_word = random.choice(wb[right_lang])

    attempt = brain.test(chosen_word)
    chosen_lang = attempt.index(max(attempt))
    if word == "":
        print("Word is from language " + lang_list[right_lang] + " !")
    print(LNeurons.repr_word(chosen_word, convert)
          + " <-- " + lang_list[chosen_lang])
    print("")
    for i in range(lang_count):
        print(lang_list[i] + ": " + str(attempt[i]))


def set_steps_menu():
    steps = []
    print("Set individual learning steps")
    p_count = int(input("Up to what pattern(old: " +
                        str(len(brain.step)) + ") : "))
    for i in range(p_count):
        if len(brain.step) > i:
            old_st = brain.step[i]
        else:
            old_st = ""
        steps.append(float(input(
            str(i + 1) + "-Letter patterns(old: "
            + str(old_st) + ") : ")))
    brain.set_step(steps)


def sentence_menu():
    sentence = input("Write here: ")
    sentence = sentence.split(" ")
    chance = [0 for x in range(lang_count)]
    for w in sentence:
        word = convert_word(0, 0, w, convert)
        i_chance = brain.test(word)
        for i in range(lang_count):
            chance[i] += i_chance[i]
    chosen_lang = chance.index(max(chance))
    print("")
    print("The Language is " + lang_list[chosen_lang] + "\n")
    for i in range(lang_count):
        print(lang_list[i] + ": " + str(chance[i] / len(sentence)))
    print("")
    input("Press ENTER to continue")


# Relatively simple menu section.
decide = 0
while True:
    print("")
    print("1 Train for x-times")
    print("2 Test success rate for x-words")
    print("3 Ask for language of a single word")
    print("4 Get Value of single pattern")
    print("5 Settings and more")
    print("6 Exit")
    decide = int(input("Decision: "))
    print("")

    if decide == 1:
        train(int(input("How many random words to train on? : ")))

    if decide == 2:
        test(int(input("How many random words to test on? : ")))

    if decide == 3:
        ask(input("Which word? (empty for random) : "))
        print("")
        input("Press ENTER to continue")

    if decide == 4:
        pos = int(input("Which position?: "))
        pattern = input("What Pattern?: ")
        brain.get_pattern(pos, pattern)
        print("")
        input("Press ENTER to continue")

    if decide == 5:
        decide2 = 0
        while decide2 != 4:
            print("")
            print("1 Edit lifesign rate")
            print("2 Learning rate per pattern")
            print("3 Text/Sentence recognition")
            print("4 Back")
            decide2 = int(input("Decision: "))
            print("")

            if decide2 == 1:
                lifesign = int(input("Rate? (default is 10000): "))

            if decide2 == 2:
                set_steps_menu()

            if decide2 == 3:
                sentence_menu()

    if decide == 6:
        print("Goodbye!")
        quit()
