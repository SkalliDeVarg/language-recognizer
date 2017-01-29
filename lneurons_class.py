class LNeurons:
    """
    This class creates easily usable neurons for language recognition.
    """
    def __init__(self, names, maxpattern):
        """
        Initializes and creates all needed parameters.
        Args:
            names (:obj:"list" of :obj:"str"): Names of the language files.
            minlength (int): Minimum length of evaluated words.
            maxlenght (int): Maximum length of evaluated words.

        Attr:
            nlang (int): count of all given language files
            step (list(float)): Determines which step size is used for which
                pattern size.
            is for evaluation for the neurons.
            ilang(list(float)): helps at initialization of neurons
            neurons(list(dict(list(float)))) : Huge list in which all
                neurons are stored.
                Neurons[i][j][k] = float value
                i = pattern position
                j = pattern
                k = language list
        """
        self.nlang = len(names)
        self.maxpattern = maxpattern
        self.names = names

        self.step = [0.001, 0.01, 0.1, 0.15, 0.2]

        self.ilang = [0.5 for i in range(self.nlang)]

        self.neurons = [dict() for i in range(3)]

        print("Init of neurons " + str(self) + " completed")

    def set_step(self, new_step):
        """Sets self.step attribute to new_step."""
        self.step = new_step

    def train(self, word, clang):
        """
        Trains the neurons on given word.

        Args:
            word (str): given word to train on.
            clang (int): given language index.
        """

        if clang < 0 or clang > self.nlang:
            print("Error, impossible Language given!")
            exit()

        word_len = len(word)
        if word_len > len(self.neurons):
            for i in range(word_len - len(self.neurons)):
                self.neurons.append(dict())

        if self.maxpattern == 0 or self.maxpattern > word_len:
            m_pat = word_len
        else:
            m_pat = self.maxpattern
        for i in range(m_pat):
            p_len = i + 1
            if i >= len(self.step):
                r_step = self.step[-1]
            else:
                r_step = self.step[i]
            f_step = r_step / (self.nlang - 1)
            for p_pos in range(word_len + 1 - p_len):
                pattern = word[p_pos:p_pos + p_len]

                if pattern not in self.neurons[p_pos]:
                    self.neurons[p_pos][pattern] = self.ilang[:]

                for k in range(self.nlang):
                    if k == clang:
                        self.neurons[p_pos][pattern][k] += r_step
                        if self.neurons[p_pos][pattern][k] > 1:
                            self.neurons[p_pos][pattern][k] = 1
                    else:
                        self.neurons[p_pos][pattern][k] -= f_step
                        if self.neurons[p_pos][pattern][k] < 0:
                            self.neurons[p_pos][pattern][k] = 0
        return

    def test(self, word):
        """
        Tests the neurons on given word.

        Args:
            word (str): given word to train on. Default "" means a random word
                gets chosen.

        Returns:
            (list(float)): individual chances arranged by language index
        """
        word_len = len(word)
        if word_len > len(self.neurons):
            for i in range(word_len - len(self.neurons)):
                self.neurons.append(dict())

        o_chance = [0 for x in range(self.nlang)]

        if self.maxpattern == 0 or self.maxpattern > word_len:
            m_pat = word_len
        else:
            m_pat = self.maxpattern
        for i in range(m_pat):
            chance = [0 for x in range(self.nlang)]
            p_len = i + 1
            poss_pos = (word_len + 1 - p_len)
            for p_pos in range(poss_pos):
                pattern = word[p_pos:p_pos + p_len]

                for k in range(self.nlang):
                    if pattern in self.neurons[p_pos]:
                        chance[k] += self.neurons[p_pos][pattern][k]
                    else:
                        chance[k] += 0.5
            for l in range(len(chance)):
                o_chance[l] += chance[l] / poss_pos
        o_chance = [x / m_pat for x in o_chance]

        # The list with individual chances per language and the chosen language
        # are returned. If no lang is given, dummy -1 gets returned for
        # chosen_lang.
        return(o_chance)

    def get_pattern(self, pos, pattern):
        pos -= 1
        if pattern in self.neurons[pos]:
            rating = self.neurons[pos][pattern]
            print(pattern + " : ")
            for i in range(len(rating)):
                print(self.names[i] + " : " + str(rating[i]))
        else:
            print("nothing found")

    @staticmethod
    def repr_word(word, convert):
        if convert is True:
            for i in range(len(word)):
                if word[i] == "[":
                    word = word[:i] + "-" + word[i + 1:]
        word = word[:-1]
        return(word)
