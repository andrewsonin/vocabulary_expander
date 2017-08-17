from expander import Expander
from exit import program_exit


def session(file):
    print('\nWelcome to Vocabulary Expander!\n'
          '\nWhich mod do you prefer?\n'
          'Just write one of the given names:\n'
          'Smart / Simple\n'
          'To exit print 0.')

    mod = input()
    mod = mod.capitalize()

    while mod != 'Simple' and mod != 'Smart':
        if mod == '0':
            program_exit()
        print('Wrong value. Try again. To exit print 0.')
        mod = input()
        mod = mod.capitalize()

    expander = Expander(file, mod)

    print('\nWhat number of words would you like to learn for each iteration?'
          '\nTo exit print value 0 or less.')

    w_num = int(input())
    if w_num <= 0:
        program_exit()

    expander.teaching(w_num)


def safe_open(file_name):
    file = open(file_name, 'r', encoding='utf8')
    temp = open('temp_' + file_name, 'w', encoding='utf8')
    temp.write(file.read())
    temp.close()
    file.close()
    return open(file_name, 'r', encoding='utf8')
