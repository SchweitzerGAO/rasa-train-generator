from typing import List, Union, Any
import os
import random


class RandomValue:
    def __init__(self, lb, ub, mode='int', precision=1):
        self.lb = lb
        self.ub = ub
        self.mode = mode
        self.precision = precision

    def rand_value(self):
        if self.mode == 'int':
            return random.randint(self.lb, self.ub)
        elif self.mode == 'float':
            return round(random.uniform(self.lb, self.ub), self.precision)
        else:
            raise ValueError(f'Mode {self.mode} is not supported!')


class Template:
    def __init__(self):
        self.sentences = []
        self.fillings = []

    def add_sentence(self, sentence_template: Union[str, List[str]]):
        """
        :param sentence_template: sentence template where labeled entities shall be in the format:
        '[{}](label)' or [{}]{entity:"entity",role:"role"}

        Example:从[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}

        :return: self
        """
        if isinstance(sentence_template, List):
            self.sentences.extend(sentence_template)
        elif isinstance(sentence_template, str):
            self.sentences.append(sentence_template)
        else:
            raise TypeError(f'Unexpected type: {type(sentence_template)}')
        return self

    def add_word(self, word_template: Union[Any, List[Any]], mode='new'):
        """
        :param word_template: words that to be formatted into the sentence template
        :param mode: 'new': add a new list of word;
                    'extend': extend the last element of the word list
        :return: self
        """
        if mode == 'new':
            self.fillings.append(word_template)
        else:
            self.fillings[-1].extend(word_template)
        return self

    def add_random_val(self, lb, ub, mode='int', precision=1):
        """
        :param lb: lower bound
        :param ub: upper bound
        :param mode: 'int': generates a random integer in range [lb,ub];
                    'float': generates a random float number in range [lb,ub];
        :param precision: The precision needed in 'float' mode
        :return: self
        """
        self.fillings.append(RandomValue(lb, ub, mode, precision))
        return self


class Generator:
    def __init__(self, intent_name):
        self.intent_name = intent_name
        self.templates = []

    def _write_file(self, sentences, to_file, mode='nlu'):
        header = f'version: "3.1"\n\n{mode}:\n'
        if not os.path.exists(to_file):
            open_mode = 'w'
        else:
            open_mode = 'a'
        with open(to_file, open_mode, encoding='utf-8') as f:
            if open_mode == 'w':
                f.write(header)
                if mode == 'nlu':
                    f.write(f'- intent: {self.intent_name}\nexamples: |\n')
                    for sentence in sentences:
                        f.write(f'    - {sentence}\n')
                else:
                    raise NotImplementedError(f'Writing {mode} data is now not supported')
            else:
                if mode == 'nlu':
                    f.write(f'\n- intent: {self.intent_name}\nexamples: |\n')
                    for sentence in sentences:
                        f.write(f'    - {sentence}\n')
                else:
                    raise NotImplementedError(f'Writing {mode} data is now not supported')

    def add_template(self, templates: Union[List[Template], Template]):
        """
        :param templates: `Template` instances
        :return: self
        """
        if isinstance(templates, List):
            self.templates.extend(templates)
        elif isinstance(templates,Template):
            self.templates.append(templates)
        else:
            raise TypeError(f'Type {type(templates)} is not supported for parameter `templates`!')
        return self

    def generate(self, n=0, to_file=None, patience=-1):
        """
        Generate training data for Rasa chat bot
        :param n: The number of sentences to generate
        :param to_file: The file to write
        :param patience: if the sentences set keeps the same for `patience` times, stop sentence generation
        :return: None
        """
        p = patience
        if n <= 0:
            raise ValueError('parameter `n` is supposed to be positive')
        if not to_file:
            raise ValueError('File to store the data shall be specified!')
        try:
            sentences = set()
            len_pre = 0
            while len(sentences) < n:
                template = random.choice(self.templates)
                sentence_template = random.choice(template.sentences)
                fillings = []
                for fill_template in template.fillings:
                    if isinstance(fill_template, List):
                        fillings.append(random.choice(fill_template))
                    elif isinstance(fill_template, RandomValue):
                        fillings.append(fill_template.rand_value())
                sentences.add(sentence_template.format(*fillings))
                if len(sentences) > len_pre:
                    len_pre += 1
                else:
                    patience -= 1
                if patience == 0:
                    print(f'Cannot add any new sentences after {p} attempts,stopped')
                    break
            self._write_file(sentences, to_file)
        except Exception as e:
            print(e)
            return
