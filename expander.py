import re
from random import shuffle, randint
from time import time
from exit import program_exit


class Expander:
    def __init__(self, file=open('dict.txt', 'r', encoding='utf8'), mod='Simple'):
        self.file = file
        self.mod = mod
        self.dict = []

        self.dict_init()
        self.dict_sorting()

    def dict_init(self, is_first=True):
        print('\nReading', self.file.name + '…')

        for line in self.file.readlines():
            # Program is matching strings of dictionary file with the sample given by regular expression
            # needed for dictionary building

            info = re.match(
                r'^(?P<word>[\w \(\)\.,\-]*) -- (?P<transl>[\w; \(\)\.,\-*|\?]+[^0-9 /,])'
                r' */*/* *(?P<rep>\d+)*,* *(?P<last_time>\d+)*$',
                line.strip())

            # Sample is like this:
            # $<some_word or expression> -- <translation><not necessary>
            # <translation> sample: {word_or_expression_1; word_or_expression_2; ...; word_or_expression_n}
            # <not necessary>: { // <number of rehearsals>, <date of the latest rehearsal>}
            # Now we have to build a list including all this information

            left = right = 0
            translation = []

            for i in range(len(info.group('transl'))):  # We must split up full translation into single words
                if info.group('transl')[i] == ';':
                    right = i
                    translation.append(info.group('transl')[left:right].strip())
                    left = right + 1
            if right != len(info.group('transl')) - 1:
                translation.append(info.group('transl')[left:].strip())

            # Now we are building self.dict with order: [word, [translations], number_of_rehearsals, latest_date]
            self.dict.append([info.group('word'), translation,
                              int(info.group('rep')) if info.group('rep') is not None else 0,
                              int(info.group('last_time')) if info.group('last_time') is not None else 0])

            # print(info.group('word'), translation, info.group('rep'), info.group('last_time'), sep='\n')

        if len(self.dict) == 0:
            print('Reading did not completed. Error occurred: Dictionary is empty\n'
                  'Please, print the location of the appropriate dictionary file.\n'
                  'To exit print 0.')
            file = input()
            if file == '0':
                program_exit()

            self.file = open(file, 'r', encoding='utf8')
            self.dict_init(False)

        if is_first:
            print('Reading completed. Errors did not occurred.')

    def dict_sorting(self):
        print('\nSorting program inner dictionary…')

        if self.mod == 'Smart':
            self.dict.sort(key=lambda x: x[2])  # sorting by number of rehearsals
            self.dict.sort(key=lambda x: x[3])  # sorting by date of the last rehearsal
        elif self.mod == 'Simple':
            shuffle(self.dict)  # randomly shuffle our dictionary
        print('Sorting completed. Errors did not occurred.')

    def teaching(self, w_num=5):

        while w_num > len(self.dict):
            print('Number of words, that you prefer to learn for each iteration, is larger than size of the '
                  'dictionary (' + str(len(self.dict)) + ').\nPlease, input another value.\n'
                  'To exit print 0 or less.')
            w_num = int(input())
            if w_num <= 0:
                program_exit()

        init = True
        cont = 'y'

        while True:
            if not init:
                print('Press "y" to continue. Other to not ("n", for example). Press 0 to exit.')
                cont = input()
            else:
                init = False
            if cont == 'y':
                self.memorizing(w_num)
                self.testing(w_num)
            elif cont == '0':
                program_exit()
            else:
                break

    def memorizing(self, w_num):
        i = 0
        while i < w_num:

            print('\n___', self.dict[i][0], '___\n')
            for word in self.dict[i][1]:
                print(word)

            while True:
                print('\nPrint "+" or "-" to go back or to go on respectively. Print "0" to exit.')
                a = input()
                if a == '+':
                    i += 1
                    break
                if a == '-':
                    i -= 1
                    if i == -1:
                        i = 0
                        print('Sorry, returning is not possible.')
                    break
                if a == '0':
                    program_exit()
                print('Try again.')

    def testing(self, w_num):
        results = [True for i in range(w_num)]
        self.__test1(w_num, results)
        self.__test2(w_num, results)
        self.__test3(w_num, results)
        self.__dict_reinit(w_num, results)
        self.rewrite()

    def __test1(self, w_num, results):
        print('\nTest 1: Choose appropriate translation of the foreign word.')
        not_used = [i for i in range(w_num)]
        shuffle(not_used)
        for cur in not_used:
            answers = ['; '.join(self.dict[randint(0, len(self.dict) - 1)][1]) for i in range(5)]

            right_answer = '; '.join(self.dict[cur][1])
            if self.dict[cur][1] not in answers:
                answers[randint(0, len(answers) - 1)] = right_answer

            print('\nChoose the right answer. (to exit print 0)')
            print('\n___', self.dict[cur][0], '___\n')
            for i in range(1, len(answers) + 1):
                print(str(i) + ':', answers[i - 1])

            while True:
                your_answer = input()
                if your_answer not in [str(i) for i in range(1, len(answers) + 1)]:
                    if your_answer == '0':
                        program_exit()
                    print('Try again. To exit print 0.')
                else:
                    break
            your_answer = int(your_answer)

            if right_answer == answers[your_answer - 1]:
                print('Correct!')
            else:
                print('Incorrect:(')
                print('Correct:', right_answer)
                results[cur] = False

    def __test2(self, w_num, results):
        print('\nTest 2: Choose appropriate translation of the native word.')
        not_used = [i for i in range(w_num)]
        shuffle(not_used)
        for cur in not_used:
            answers = [self.dict[randint(0, len(self.dict) - 1)][0] for i in range(5)]

            right_answer = self.dict[cur][0]
            if self.dict[cur][0] not in answers:
                answers[randint(0, len(answers) - 1)] = right_answer

            print('\nChoose the right answer. (to exit print 0)')
            print('\n___', '; '.join(self.dict[cur][1]), '___\n')
            for i in range(1, len(answers) + 1):
                print(str(i) + ':', answers[i - 1])

            while True:
                your_answer = input()
                if your_answer not in [str(i) for i in range(1, len(answers) + 1)]:
                    if your_answer == '0':
                        program_exit()
                    print('Try again. To exit print 0.')
                else:
                    break
            your_answer = int(your_answer)

            if right_answer == answers[your_answer - 1]:
                print('Correct!')
            else:
                print('Incorrect :-(')
                print('Correct:', right_answer)
                results[cur] = False

    def __test3(self, w_num, results):
        print('\nTest 3: Translate native word.')
        not_used = [i for i in range(w_num)]
        shuffle(not_used)
        for cur in not_used:
            answers = [self.dict[randint(0, len(self.dict) - 1)][0] for i in range(5)]

            right_answer = self.dict[cur][0]
            if self.dict[cur][0] not in answers:
                answers[randint(0, len(answers) - 1)] = right_answer

            while True:
                print('\nPrint the translation. To pass this word print "p". (to exit print 0)')
                print('\n___', '; '.join(self.dict[cur][1]), '___\n')
                your_answer = input()
                if your_answer == 'p':
                    results[cur] = False
                    break
                if your_answer == '0':
                    program_exit()
                if your_answer == right_answer:
                    print('Correct!')
                    break
                else:
                    print('Incorrect :-(')
                    print('Try again.')
                    results[cur] = False

    def __dict_reinit(self, w_num, results):
        cur_time = int(time())
        for i in range(w_num):
            if results[i]:
                self.dict[i][2] += 1
                self.dict[i][3] = cur_time
        self.dict.extend(self.dict[:w_num])
        for i in range(w_num):
            self.dict.pop(0)

    def rewrite(self):
        self.file.close()
        self.file = open(self.file.name, 'w', encoding='utf8')
        for data in self.dict:
            self.file.write(str(data[0]) + ' -- ' + '; '.join(data[1]) +
                            ' // ' + str(data[2]) + ', ' + str(data[3]) + '\n')
        print('All progress saved successfully.\n')
        self.file.close()
        self.file = open(self.file.name, 'r', encoding='utf8')
