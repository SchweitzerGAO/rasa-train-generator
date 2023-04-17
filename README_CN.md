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

**创建`Template`**



**使用`Generator`**

