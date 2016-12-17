from lneurons_class import LNeurons

# For initialization all parameters are prompted.
print("Welcome to Leif's neuron based language recognizer with dynamically "
      "stacked pattern size. Everything should be quite self explanatory, but "
      "be sure to use 4 for pattern length or less for faster but less "
      "accurate prediction. Values above 4 WILL congest your RAM.")

plength = int(input("Pattern length: "))
print("Minimum word length must be at least " + str(plength - 1) + " !")
minlength = int(input("Minimum length of words: "))
maxlength = int(input("Maximum length of words: "))
word_count = int(input("How many languages to learn: "))
lang_list = []
for i in range(word_count):
    lang_list.append(input("Name of language file: "))
brain = LNeurons(lang_list, minlength, maxlength, plength)

lifesign = 10000


def train(length):
    """
    This function calls the brain.train() function n times and prints
    progress all lifesign calls.
    """
    for i in range(1, length + 1):
        brain.train()
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
    indiv_success = [[] for i in range(brain.nlang)]
    for i in range(1, length + 1):
        # The validity of the chosen language of the neurons is evaluated and
        # saved in two seperate arrays.
        attempt = brain.test()
        chosen_lang = attempt[2].index(max(attempt[2]))
        if chosen_lang == attempt[1]:
            choice = 1
        else:
            choice = 0

        success_list.append(choice)
        indiv_success[attempt[1]].append(choice)
        if i % lifesign == 0 or i == length:
            print("Progress: "
                  + str(i / length * 100) + "%    "
                  + "Total success: "
                  + str(sum(success_list) / len(success_list) * 100)
                  + "%")
    print("")
    for i in range(brain.nlang):
        # This prevents division by zero.
        if len(indiv_success[i]) > 0:
            print(brain.names[i] + " success: "
                  + str(sum(indiv_success[i]) / len(indiv_success[i]) * 100)
                  + "%")
        else:
            print(brain.names[i] + " no sufficient data")
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
        word = brain.convert_word(word)
    # When brain.test(""), a random word gets chosen.
    attempt = brain.test(word)
    chosen_lang = attempt[2].index(max(attempt[2]))
    if word == "":
        print("Word is from language " + brain.names[attempt[1]] + " !")
    print(LNeurons.repr_word(attempt[0]) + " <-- " + brain.names[chosen_lang])
    print("")
    for i in range(len(brain.names)):
        print(brain.names[i] + ": " + str(attempt[2][i]))

# Relatively simple menu section.
decide = 0
while True:
    print("")
    print("1 Train for x-times")
    print("2 Test success rate for x-words")
    print("3 Ask for language of a single word")
    print("4 Edit settings")
    print("5 Exit")
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
        decide2 = 0
        while decide2 != 4:
            print("")
            print("1 Edit lifesign rate")
            print("2 Learning rate per pattern")
            print("3 Custom rating per pattern")
            print("4 Back")
            decide2 = int(input("Decision: "))
            print("")

            if decide2 == 1:
                lifesign = int(input("Rate? (default is 10000): "))

            if decide2 == 2:
                steps = []
                print("Set individual learning steps (default is 0.00001, "
                      "0.0001, 0.001, 0.01)")
                for i in range(brain.plength):
                    steps.append(float(input(str(i + 1)
                                             + "-Letter patterns: ")))
                brain.set_step(steps)

            if decide2 == 3:
                ratings = []
                print("Set individual ratings (default is 1.0)")
                for i in range(brain.plength):
                    ratings.append(float(input(str(i + 1)
                                               + "-Letter ratings: ")))
                brain.set_rating(ratings)

    if decide == 5:
        print("Goodbye!")
        quit()
