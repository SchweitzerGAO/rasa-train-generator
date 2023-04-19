from rasa_gen import NLUTemplate, Generator

if __name__ == '__main__':
    '''
    generate from template
    '''
    sentence_template = [
        '[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '把[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '空调[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '把空调[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',

    ]
    word_template = [
        '温度降低到', '温度升高到', '温度升高至', '温度降低至', '温度调整到', '温度调整至', '温度调到', '温度调至',
    ]
    template = NLUTemplate().add_sentence(sentence_template) \
        .add_word(word_template) \
        .add_random_val(16, 30)
    generator = Generator('test_intent').add_template(template)
    generator.generate_from_template(50, './tests/test_template.yml')

    '''
    generate from .txt file
    '''
    generator.set_key('test_lookup')
    generator.generate_from_file('./tests/test.txt', './tests/test_txt.yml')

    '''
    generate from .csv and .tsv file
    '''
    generator.set_key()
    generator.generate_from_file('./tests/test.csv', 'tests/test_csv.yml')
    generator.generate_from_file('./tests/test.tsv', 'tests/test_tsv.yml')
