import pickle
import random


class model:

    def __init__(self):
        self.model = dict()
        self.len_prefix = 1  # this code work if len_prefix = only 1
        self.amount_start_words = 0
        self.start_words = []  # all words, which begin sentences

    def create_model(self, text):
        text = text.split(sep=".", maxsplit=3)

        for sentence in text:
            bad_chars = '''!.,?#@;:`""“\n” '''
            word = ""
            words_in_sentence = list()
            for char in sentence:
                if char in bad_chars:
                    if word != "":
                        words_in_sentence.append(word.lower())
                    word = ""
                else:
                    word += char
            if word != "":
                words_in_sentence.append(word.lower())

            if len(words_in_sentence) == 0:
                continue

            self.start_words.append(words_in_sentence[0])
            self.amount_start_words += 1
            self.model["."] = self.model.get(".", list())
            self.model["."].append(words_in_sentence[0])  # after '.' begin new sentence

            for index in range(len(words_in_sentence)):
                word = words_in_sentence[index]
                if index + 1 < len(words_in_sentence):
                    self.model[word] = self.model.get(word, list())
                    next_word = words_in_sentence[index + 1]
                    self.model[word].append(next_word)
                else:
                    self.model[word] = self.model.get(word, list())
                    self.model[word].append(".")  # this is end of sentence

    def generate_start_word(self):
        random_index = random.randint(1, self.amount_start_words) - 1  # transform to 0-indexing
        start_prefix = self.start_words[random_index]
        return start_prefix

    def generate_next_word(self, word):
        random_index = random.randint(1, len(self.model[word])) - 1  # transform to 0-indexing
        return self.model[word][random_index]

    def generate_text(self, length):
        last_word = self.generate_start_word()
        text = last_word + " "
        for i in range(1, length):
            next_word = self.generate_next_word(last_word)
            text += next_word + " "
            last_word = next_word
        return text


def read_model():
    with open("model.pickle", "rb") as f:
        sample = pickle.load(f)
        return sample


def main():
    sample = read_model()
    length = random.randint(500, 500)
    generated_text = sample.generate_text(length)
    print(generated_text)


if __name__ == '__main__':
    main()
