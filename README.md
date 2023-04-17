# RasaGen: A [Rasa](https://github.com/RasaHQ/rasa) chatbot training data generator
([中文版](README_CN.md)) | (English)
## Installation

Install the latest version of `RasaGen` by running:
```
pip install rasa_gen
```
or install with source code:
```
pip install git+https://github.com/SchweitzerGAO/rasa-train-generator
```
## Usage
**An Example**

_Though the template in this example is in Chinese, It supports mainstream languages_
```python
from rasa_gen import Template, Generator

if __name__ == '__main__':
    sentence_template = [
        '[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '把[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '空调[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '把空调[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',

    ]
    word_template = [
        '温度降低到', '温度升高到', '温度升高至', '温度降低至', '温度调整到', '温度调整至', '温度调到', '温度调至',
    ]
    template = Template().add_sentence(sentence_template) \
                         .add_word(word_template) \
                         .add_random_val(16, 30)
    generator = Generator('test_intent').add_template(template)
    generator.generate(50, './test.yml')
```
**Creating a `Template`**

As shown in the example, 
you can create a template by creating a `Template` instance and add sentence, 
word and random value templates in a stream 

**Using a `Generator`**

