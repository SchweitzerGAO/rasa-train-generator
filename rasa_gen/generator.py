from typing import List, Union


class Template:
    def __init__(self):
        self.sentences = []
        self.words = []

    def add_sentence(self, sentence_template: Union[str, List[str]]):
        if isinstance(sentence_template, str):
            self.sentences.extend([sentence_template])
        else:
            self.sentences.extend(sentence_template)
        return self

    def add_word(self, word_template: Union[str, List[str]]):
        if isinstance(word_template, str):
            self.words.extend([word_template])
        else:
            self.words.extend(word_template)
        return self


class Generator:
    def __init__(self, intent_name):
        self.intent_name = intent_name
        self.templates = []

    def add_template(self, templates: List[Template]):
        self.templates.extend(templates)
        return self

    def generate(self, n, to_file):
        sentences = set()




