import random
from wordbooks import wordbooks_ask
from wordbooks import check_word
from wordbooks import convert
from wordbooks import check_all


class LNeurons:
    """
    This class creates easily usable neurons for language recognition.
    """
    def __init__(self, names, minlength, maxlength, plength=4):
        """
        Initializes and creates all needed parameters.
        Args:
            names (:obj:"list" of :obj:"str"): Names of the language files.
            minlength (int): Minimum length of evaluated words.
            maxlenght (int): Maximum length of evaluated words.
            plength (int): Maximum size of the biggest pattern used.

        Attr:
            nlang (int): count of all given language files
            wb (list(list(str))): All wordbooks sorted by language and readily
                formatted with A-Z letters.
            step (list(float)): Determines which step size is used for which
                pattern size.
            rating(list(float)): Determines how "important" each pattern size
            is for evaluation for the neurons.
            ilang(list(float)): helps at initialization of neurons
            neurons(list(list(list(list(float))))) : Huge list in which all
                neurons are stored.
                Neurons[i][j][k][l] = float value
                i = pattern length
                j = letter position
                k = letter value (A-Z)
                l = language index
        """
        self.nlang = len(names)
        self.minlength = minlength + 1
        self.maxlength = maxlength + 1
        self.plength = plength
        self.names = names

        if self.minlength < plength:
            print("Error, minimum word length has to be bigger or equal "
                  "to pattern length")
            quit()

        self.wb = wordbooks_ask(self.nlang, self.minlength - 1,
                                self.maxlength - 1, names)

        self.step = [0.00001, 0.0001, 0.001, 0.01]
        self.rating = [1, 1, 1, 1]

        self.ilang = [1 / self.nlang for i in range(self.nlang)]

        self.neurons = [[[list(self.ilang) for i in range(27**(k + 1))]
                         for j in range(self.maxlength - k)]
                         for k in range(self.plength)]

        print("Init of neurons " + str(self) + " completed")

    def set_step(self, new_step):
        """Sets self.step attribute to new_step."""
        if len(new_step) == self.plength:
            self.step = new_step
        else:
            print("Error: wrong count of step values given")

    def set_rating(self, new_rating):
        """Sets self.rating attribute to new_rating."""
        if len(new_rating) == self.plength:
            self.rating = new_rating
        else:
            print("Error: wrong count of rating values given")

    def train(self, word="", clang=-1):
        """
        Trains the neurons on given word.

        Args:
            word (str): given word to train on. Default "" means a random word
                gets chosen.
            clang (int): given language index which gets passed.

        Returns:
            list: list[0] = (str): word on which was trained on.
                  list[1] = (int): language index of word.
        """

        if word == "":
            # One out of the given languages is randomly chosen.
            chosen_lang = random.choice(list(range(self.nlang)))

            # One random word out of the chosen language is chosen.
            chosen_word = random.choice(self.wb[chosen_lang])
        else:
            if clang < 0 or clang > self.nlang:
                print("Error, impossible Language given!")
                exit()
            chosen_lang = clang
            chosen_word = word

        # The word gets converted to an integer list with A = 0 and Z = 25.
        word_index = [ord(letter) - 65 for letter in chosen_word]

        # i = individual pattern length
        # j = letter position corrected per indiv. pattern
        # k = individual languages
        for i in range(self.plength):
            for j in range(len(word_index) - i):
                index = 0
                for z in range(i + 1):
                    # The index number for single and combined letters gets
                    # determined by multiplying and adding up.
                    index += word_index[j + z] * 27**z
                for k in range(self.nlang):
                    if k == chosen_lang:
                        self.neurons[i][j][index][k] += self.step[i]

                        if self.neurons[i][j][index][k] > 1:
                            self.neurons[i][j][index][k] = 1
                    else:
                        self.neurons[i][j][index][k] \
                            -= self.step[i] / (self.nlang - 1)

                        if self.neurons[i][j][index][k] < 0:
                            self.neurons[i][j][index][k] = 0

        return([chosen_word, chosen_lang])

    def test(self, word="", clang=-1):
        """
        Tests the neurons on given word.

        Args:
            word (str): given word to train on. Default "" means a random word
                gets chosen.
            clang (int): given language index which gets passed.

        Returns:
            list: list[0] = (str): word on which was trained on.
                  list[1] = (int): language index of word.
                  list[2] = (list(float)): individual chances arranged by
                            language index
        """

        if word == "":
            # One out of the given languages is randomly chosen.
            chosen_lang = random.choice(list(range(self.nlang)))

            # On random word out of the chosen language is chosen.
            chosen_word = random.choice(self.wb[chosen_lang])
        else:
            chosen_lang = clang
            chosen_word = word

        # The word gets converted to an integer list with A = 0 and Z = 25.
        word_index = [ord(letter) - 65 for letter in chosen_word]

        # The list for overall chance gets initialised.
        o_chance = [0 for x in range(self.plength)]

        # i = individual pattern length
        # j = letter position corrected per indiv. pattern
        # k = individual languages
        for i in range(self.plength):
            chance = [0 for x in range(self.nlang)]
            for j in range(len(word_index) - i):
                index = 0
                for z in range(i + 1):
                    # The index number for single and combined letters gets
                    # determined by multiplying and adding up.
                    index += word_index[j + z] * 27**z
                for k in range(self.nlang):
                    # The individual chances as determined in 'Neurons' add up
                    # per language.
                    chance[k] += self.neurons[i][j][index][k]

            # Chances are divided by individual count of letter positions.
            # The different Ratings per pattern are also applied.
            chance = [x / (len(word_index) - i) * self.rating[i]
                      for x in chance]
            # Chances per pattern are collected in o_chance
            o_chance[i] = chance

        # All pattern chances add up to one individual language chance and are
        # divided by the pattern count.
        chance = [0 for x in range(self.nlang)]
        for i in range(self.nlang):
            chance[i] = sum([o_chance[x][i] for x in range(self.plength)]) \
                        / self.plength

        # The list with individual chances per language and the chosen language
        # are returned. If no lang is given, dummy -1 gets returned for
        # chosen_lang.
        return([chosen_word, chosen_lang, chance])

    def check_word(self, word):
        """
        Checks if word consists of only A-Z and is the right length.

        Args:
            word (str): given word to check

        Returns:
            int: 0 if failed 1 for success
        """
        return (check_word(self.minlength, self.maxlength, word))

    def convert_word(self, word):
        """Converts given word to A-Z format and checks length"""
        return (convert(self.minlength - 1, self.maxlength - 1, word))

    @staticmethod
    def check_all():
        """Checks for foreign letters in wordlist"""
        check_all()

    @staticmethod
    def repr_word(word):
        for i in range(len(word)):
            if word[i] == "[":
                word = word[:i] + "-" + word[i + 1:]
        word = word[:-1]
        return(word)
