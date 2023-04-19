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
## Basic usage
**An Example**

_Though the template in this example is in Chinese, It supports mainstream languages like English, French and Japanese etc._

```python
from rasa_gen import NLUTemplate, Generator

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
    template = NLUTemplate().add_sentence(sentence_template)\
                            .add_word(word_template)\
                            .add_random_val(16, 30)
generator = Generator('test_intent').add_template(template)
generator.generate_from_template(50, './test_template.yml')
```
A detailed example is in `example.py`


**Creating a `NLUTemplate`**

As shown in the example, 
you can create a NLU training data generating template by creating a `NLUTemplate` instance and add sentence, 
word and random value to fill 
in the template in a streaming way.

**Using a `Generator`**

1. Create a `Generator`

You can create a `Generator` instance 
with specifying the name of the key of the training data. 
For example, 
you shall specify the name of `intent` 
when generating data for an intent
or the name of `lookup` for a lookup table.

**Note: If you are generating data from a csv or tsv file 
with the name of `lookup` in the first column, 
there is no need to specify 
the name when creating a `Generator`**

For now, only `intent` and `lookup` data types in `nlu` class are supported.
Other types like `rule` and `story` 
will be supported in the future

2. Generate data by a `Generator`

There are 2 supported ways to generate data by a `Generator`
- From a template (Recommended for `intent` data)

You can add a `Template` instance by `add_template` method and generate the data by `generate_from_template` method.

- From a file (Recommended for `lookup` data)

There is no need to create `Template` instances. 
Just specify the input file and output file 
and use the `generate_from_file` method will be OK. 

## Coming Soon...
- Generating `story`, `synonym` and `rule` data

- The detailed [document](https://github.com/SchweitzerGAO/rasa-train-generator) will be released soon.