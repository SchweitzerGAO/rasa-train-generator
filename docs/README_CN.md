# RasaGen: 一个 [Rasa](https://github.com/RasaHQ/rasa) 聊天机器人训练数据生成工具

(中文版)|([English](README.md))

## 安装

可通过运行
```
pip install rasa_gen
``` 

安装最新版本

或可运行
```
pip install git+https://github.com/SchweitzerGAO/rasa-train-generator
```
以通过源码安装

## 使用方法

**程序示例**

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
更详细的示例见`example.py`

**创建`NLUTemplate`**

创建`NLUTemplate`时，需要通过`add_sentence`方法指定句子模板，
通过`add_word`方法指定向句子模板内填充的词语列表
通过`add_random_val`方法在句子中填充随机数

**使用`Generator`**

1. 创建`Generator`


2. 生成训练数据

## 即将推出

- 对`synonym`, `rule`, `story`等数据生成的支持
- 更加详细的[使用文档](https://github.com/SchweitzerGAO/rasa-train-generator)