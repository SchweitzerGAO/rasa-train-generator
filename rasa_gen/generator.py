from typing import List, Union, Any, Dict, Set
import os
import random
import cn2an
import pandas as pd


class _RandomValueGenerator:
    def __init__(self, lb, ub, mode='int', precision=1, p_cn=0.0):
        self.lb = lb
        self.ub = ub
        self.mode = mode
        self.precision = precision
        if p_cn < 0:
            print('Parameter p_cn is supposed to be in range [0,1],setting this to 0')
            self.p_cn = 0
        elif p_cn > 1:
            print('Parameter p_cn is supposed to be in range [0,1],setting this to 1')
            self.p_cn = 1
        else:
            self.p_cn = p_cn

    def rand_value(self):
        if self.mode == 'int':
            ret = random.randint(self.lb, self.ub)
        elif self.mode == 'float':
            ret = round(random.uniform(self.lb, self.ub), self.precision)
        else:
            raise ValueError(f'Mode {self.mode} is not supported')
        if random.random() < self.p_cn:
            ret = cn2an.an2cn(ret)
        return ret


class NLUTemplate:
    def __init__(self):
        self.sentences = []
        self.fillings = []

    def add_sentence(self, sentence_template: Union[str, List[str]]):
        """
        Add sentence templates
        :param sentence_template: sentence template where labeled entities shall be in the format:'[{}](label)' or [{}]{entity:"entity",role:"role"}
        >>> # an example sentence template
        >>> example = '从[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}'
        :return: self
        """
        if isinstance(sentence_template, List):
            self.sentences.extend(sentence_template)
        elif isinstance(sentence_template, str):
            self.sentences.append(sentence_template)
        else:
            raise TypeError(f'Unexpected type: {type(sentence_template)}')
        return self

    def add_word(self, word_template: Union[Any, List[Any]], mode: str = 'new'):
        """
        Add word templates corresponding to a sentence template
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

    def add_random_val(self,
                       lb: Union[int, float],
                       ub: Union[int, float],
                       mode: str = 'int',
                       precision: int = 1,
                       p_cn: float = 0.0):
        """
        Add a random number generator
        :param lb: lower bound
        :param ub: upper bound
        :param mode: 'int': generates a random integer in range [lb,ub];
                    'float': generates a random float number in range [lb,ub];
        :param precision: The precision needed in 'float' mode
        :param p_cn: The probability that a number is converted to Chinese
        :return: self
        """
        self.fillings.append(_RandomValueGenerator(lb, ub, mode, precision, p_cn))
        return self


class Generator:
    def __init__(self, key_name: str = None):
        if key_name and not isinstance(key_name, str):
            raise TypeError(f'Type {type(key_name)} is not supported for `key_name`')
        self._key_name = key_name
        self._templates = []
        self._data: Union[List, Dict, Set] | None = None

    def _read_txt(self, from_file):
        self._data = []
        with open(from_file, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                self._data.append(line)

    def _read_csv(self, from_file, mode, has_header):
        self._data = dict()
        if mode == 'csv':
            sep = ','
        else:
            sep = '\t'
        if not has_header:
            df = pd.read_csv(from_file, sep=sep, names=['k', 'v'])
        else:
            df = pd.read_csv(from_file, sep=sep, names=['k', 'v'], header=0)
        for _, row in df.iterrows():
            if row['k'] not in self._data.keys():
                self._data[row['k']] = [row['v']]
            else:
                self._data[row['k']].append(row['v'])

    def _write_file(self, to_file, cls, key):
        if cls == 'nlu':
            header = f'version: "3.1"\n\n{cls}:\n'
            if not os.path.exists(to_file):
                open_mode = 'w'
            else:
                open_mode = 'a'
            with open(to_file, open_mode, encoding='utf-8') as f:
                if open_mode == 'w':
                    f.write(header)
                if self._key_name:
                    f.write(f'- {key}: {self._key_name}\n  examples: |\n')
                if key == 'intent':
                    for item in self._data:
                        f.write(f'    - {item}\n')
                    f.write('\n')
                elif key == 'lookup':
                    if isinstance(self._data, list):
                        if not self._key_name:
                            raise ValueError('Please specify the key name of this part of data.')
                        for item in self._data:
                            f.write(f'    - {item}')
                    elif isinstance(self._data, set):
                        if not self._key_name:
                            raise ValueError('Please specify the key name of this part of data.')
                        for item in self._data:
                            f.write(f'    - {item}\n')
                    elif isinstance(self._data, dict):
                        for k in self._data.keys():
                            f.write(f'- {key}: {k}\n  examples: |\n')
                            for v in self._data[k]:
                                f.write(f'    - {v}\n')
                            f.write('\n')
                else:
                    raise NotImplementedError(f'Writing {key} data is not supported for now')
        else:
            raise NotImplementedError(f'Writing {cls} data is not supported for now')

    def set_key(self, new_key: str = None):
        """
        :param new_key: The new key for the generator
        :return: None
        """
        if new_key and not isinstance(new_key, str):
            raise TypeError(f'Type {type(new_key)} is not supported for `key_name`')
        self._key_name = new_key

    def add_template(self, templates: Union[List[NLUTemplate], NLUTemplate]):
        """
        Add a ``[CLS]Template`` instance to generate data.

        ``[CLS]`` is in ['NLU','Synonym','Story','Rule']. Now only ``NLUTemplate`` is supported
        :param templates: ``[CLS]Template`` instances
        :return: self
        """
        if isinstance(templates, List):
            self._templates.extend(templates)
        elif isinstance(templates, NLUTemplate):
            self._templates.append(templates)
        else:
            raise TypeError(f'Type {type(templates)} is not supported for parameter `templates`!')
        return self

    def generate_from_template(self,
                               n: int = 0,
                               to_file: str = None,
                               patience: int = -1,
                               cls: str = 'nlu',
                               key: str = 'intent'):
        """
        Generate training data for Rasa chatbot from a ``[CLS]Template`` instance

        ``[CLS]`` is in ['NLU','Synonym','Story','Rule']. Now only ``NLUTemplate`` is supported
        :param n: The number of ``self.data`` to generate
        :param to_file: The file in which the data will be stored.
        :param patience: If the ``self.data`` set keeps the same for ``patience`` times, stop sentence generation
        :param cls: The class of the training data. Example: "nlu"
        :param key: The key for this class. Example: "lookup","intent"
        :return: None
        """
        p = patience
        if len(self._templates) == 0:
            raise ValueError('The template of this generator is empty')
        if n <= 0:
            raise ValueError('parameter `n` is supposed to be positive')
        if not to_file:
            raise ValueError('File to store the data shall be specified')
        try:
            self._data = set()
            len_pre = 0
            while len(self._data) < n:
                template = random.choice(self._templates)
                sentence_template = random.choice(template.sentences)
                fillings = []
                for fill_template in template.fillings:
                    if isinstance(fill_template, List):
                        fillings.append(random.choice(fill_template))
                    elif isinstance(fill_template, _RandomValueGenerator):
                        fillings.append(fill_template.rand_value())
                self._data.add(sentence_template.format(*fillings))
                if len(self._data) > len_pre:
                    len_pre += 1
                else:
                    patience -= 1
                if patience == 0:
                    print(f'Could not add any new self.data after {p} attempts. '
                          f'Added {len(self._data)} items'
                          f'Writing current data to file')
                    break
            self._write_file(to_file, cls, key)
            self._data.clear()
        except Exception as e:
            print(e)
            return

    def generate_from_file(self,
                           from_file: str = None,
                           to_file: str = None,
                           has_header: bool = False,
                           cls: str = 'nlu',
                           key: str = 'lookup'):
        """
        Generate the training data from file
        :param from_file: The file from which the data will be read
        :param to_file: The file in which the data will be stored.
        :param has_header: only used in .csv and .tsv files, indicating if there is a header.
        :param cls: The class of the training data. Now supported: "nlu"
        :param key: The key for this ``cls``. Now supported: "lookup","intent"
        :return: None
        """
        supported_format = ['txt', 'csv', 'tsv']
        if not from_file:
            raise ValueError('Please specify a file to read the data')
        if not to_file:
            raise ValueError('Please specify a file to write the data')
        file_fmt = from_file.split('.')[-1].lower()
        if file_fmt not in supported_format:
            raise TypeError(f'"{file_fmt}" is not supported for now')
        if file_fmt == 'txt':
            self._read_txt(from_file)
        elif file_fmt == 'csv' or file_fmt == 'tsv':
            self._read_csv(from_file, file_fmt, has_header)
        self._write_file(to_file, cls, key)
        self._data.clear()
