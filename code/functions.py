import os

class word():
    pass

def cut_filename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def get_filenames_from_folder(folder_path):
    import glob
    # directory = os.fsencode(folder_path)  
    for i, file in enumerate(glob.glob(folder_path + '*')):
        # print(i, file, 'xxx')
        yield file

def create_filename_list(foldername = '../data/Official_HSK/', from_level = 1, to_level = 5):
    return [foldername + 'HSK' + str(x) + '.csv' for x in range(from_level, to_level + 1)]

def rename_files_in_folder(folder_path):  
    for i, file in enumerate(os.listdir(folder_path)):
        os.rename(folder_path + '/' + str(file), str(i)+'_.txt')

def line_to_word(line):
    """
        This function takes a line in format
        汉字 [han zi] - Chinese character, hieroglyph
        and transforms into a word object with
        w.chinese = '汉字'
        w.pinyin = 'han zi'
        w.translation = ['Chinese character', 'hieroglyph']
    """
    new_word = word()       
    line_stripped = line.strip()
    
    new_word.chinese = line_stripped[:line_stripped.find(' ')].strip()

    if '[' in line_stripped and ']' in line_stripped:
        new_word.pinyin = line_stripped[line_stripped.find('[')+1:line_stripped.find(']')].strip()
    else:
        new_word.pinyin = None

    line_stripped = line_stripped[line_stripped.find(']') + 1:]
    if '(' in line_stripped:
        # print(line)
        line_before_bracket = line_stripped[:line_stripped.find('(')].strip()
        if ')' in line_stripped:
            bracketed_subline = line_stripped[line_stripped.find('('):line_stripped.find(')') + 1].strip()
            line_after_bracket = line_stripped[line_stripped.find(')')+1:].strip()
        else:
            bracketed_subline = line_stripped[line_stripped.find('('):].strip()
            line_after_bracket = ''

        if ',' in line_before_bracket:
            attached_word_before = line_before_bracket[line_before_bracket.rfind(','):].strip()
            line_before_bracket = line_before_bracket[:line_before_bracket.rfind(',')].strip()
        else:
            attached_word_before = line_before_bracket[line_before_bracket.rfind('- ') + 2:].strip()
            line_before_bracket = line_before_bracket[:line_before_bracket.find('- ')]

        if ',' in line_after_bracket:
            attached_word_after = line_after_bracket[:line_after_bracket.find(',')].strip()
            line_after_bracket = line_after_bracket[line_after_bracket.find(','):].strip()
        else:
            attached_word_after = line_after_bracket.strip()
            line_after_bracket = ''

        bracketed_subline = (attached_word_before + ' ' + bracketed_subline + ' ' + attached_word_after).strip()
        line_before = line_before_bracket[line_stripped.find('-')+1:].strip()
        line_after = line_after_bracket.strip()
        trans_before = []
        trans_after = []
        if len(line_before) > 0:
            trans_before = line_before.split(', ')
        if len(line_after) > 0:
            trans_after = line_after.split(', ')
        translation = trans_before + [bracketed_subline] + trans_after
        new_translation = []
        for tr in translation:
            if len(tr) > 0:
                new_translation.append(tr)

        new_word.translation = new_translation
        return new_word
    else:
        new_word.translation = line_stripped[line_stripped.find('-')+1:].strip().split(', ')
        return new_word
    

def file_to_list_of_words(filename):
    list_of_words = []
    with open(filename, encoding='utf8') as data_file:
        first_line = data_file.readline()
        line = data_file.readline()
        while line:
            if len(line) > 1:
                new_word = line_to_word(line)
                list_of_words.append(new_word)
            line = data_file.readline()

    return list_of_words


def csv_to_list_of_words(filename):
    list_of_words = []
    import pandas as pd
    data = pd.read_csv(filename)
    data.reset_index()
    for index, row in data.iterrows():
        w = word()
        w.chinese = row['Chinese'].strip()
        w.pinyin = row['Pinyin'].strip()
        w.translation = row['English'].split(';')
        w.filename = cut_filename(filename)
        list_of_words.append(w)
    return list_of_words


def folder_to_list_of_words(foldername):
    list_of_all_words = []
    for filename in get_filenames_from_folder(foldername):
        list_of_words = file_to_list_of_words(filename)
        list_of_all_words += list_of_words

    return list_of_all_words


def word_to_string(w):
    """
        This function transforms a word object into a string for output
    """


    word_string = w.chinese

    if w.pinyin is not None:
        word_string += ' '*(6 - len(w.chinese)) + '\t [' + w.pinyin + '] - \t'
    else:
        word_string += ' - '

    for tr in w.translation:
        word_string += tr + ', '
    return(word_string[:-2])


def detect_and_count_multiple_entry_words(list_of_all_words):
    list_of_chinese_words = [x.chinese for x in list_of_all_words]
    set_of_chinese_words = set(list_of_chinese_words)

    print('Unique words: ', len(set_of_chinese_words))
    print('Total number of words: ', len(list_of_all_words))

    chinese_to_word = {}
    for w in list_of_all_words:
        if w.chinese not in chinese_to_word.keys():
            chinese_to_word[w.chinese] = w
        else:
            chinese_to_word[w.chinese].translation = list(set(w.translation + chinese_to_word[w.chinese].translation))

    word_to_count = {w: 0 for w in set_of_chinese_words}
    for w in list_of_chinese_words:
        word_to_count[w] += 1

    list_of_unique_words = sorted(list(set_of_chinese_words), key=lambda x: word_to_count[x], reverse=True)
    counter = 1
    for w in list_of_unique_words:
        if word_to_count[w] > 1:
            counter += 1
            print(word_to_count[w], word_to_string(chinese_to_word[w]))
    print(counter)


def create_list_of_unique_words(list_of_all_words):
    list_of_chinese_words = [x.chinese for x in list_of_all_words]
    set_of_chinese_words = set(list_of_chinese_words)

    chinese_to_word = {}
    for w in list_of_all_words:
        if w.chinese not in chinese_to_word.keys():
            chinese_to_word[w.chinese] = w
        else:
            chinese_to_word[w.chinese].translation = list(set(w.translation + chinese_to_word[w.chinese].translation))

    word_to_count = {w: 0 for w in set_of_chinese_words}
    for w in list_of_chinese_words:
        word_to_count[w] += 1

    list_of_unique_words_chinese = sorted(list(set_of_chinese_words), key=lambda x: word_to_count[x], reverse=True)
    counter = 1
    for w in list_of_unique_words_chinese:
        if word_to_count[w] > 1:
            counter += 1

    list_of_unique_words = []
    for w in word_to_count:
        list_of_unique_words.append(chinese_to_word[w])
    
    return list_of_unique_words


def character_to_words(list_of_all_words):
    list_of_unique_words = create_list_of_unique_words(list_of_all_words)

    character_to_words = {}
    for w in list_of_unique_words:
        characters = set(list(w.chinese))
        
        for ch in characters:
            if ('（' not in ch) and ('）' not in ch):
                if ch not in character_to_words.keys():
                    character_to_words[ch] = [w]
                else:
                    character_to_words[ch].append(w)
    return character_to_words
    

def output_words_to_file(list_of_words, filename, title='Default title'):
    with open(filename, 'w', encoding='utf8') as file_to_write:
        file_to_write.write(title + ' \n')
        for w in list_of_words:
            file_to_write.write(word_to_string(w) + '\n')


def print_words_by_character_with_frequencies(list_of_all_words, lowest_frequency = 2):
    ch_to_w = character_to_words(list_of_all_words)
    print('Total number of characters ', len(ch_to_w.keys()))

    characters = sorted(list(ch_to_w.keys()), key=lambda x: len(ch_to_w[x]), reverse=True)

    for ch in characters:
        if len(ch_to_w[ch]) > lowest_frequency:
            print('==========================')
            print('Character ', ch, ' occurs in ', len(ch_to_w[ch]), ' unique words:')
            for w in ch_to_w[ch]:
                print(word_to_string(w))


def save_words_by_character_with_frequencies_to_file(list_of_all_words, filename='all_words_by_character_frequency.txt'):
    ch_to_w = character_to_words(list_of_all_words)
    with open(filename, 'w') as out_file:
        
        out_file.write('Total number of characters ' + str(len(ch_to_w.keys())) + '\n')

        characters = sorted(list(ch_to_w.keys()), key=lambda x: len(ch_to_w[x]), reverse=True)

        for ch in characters:
            out_file.write('==========================\n')
            out_file.write('Character ' + ch + ' occurs in ' + str(len(ch_to_w[ch])) + ' unique words:\n')
            for w in ch_to_w[ch]:
                out_file.write(word_to_string(w) + '\n')
    



if __name__ == "__main__":

    # foldername = 'D:\Chinese_vocabulary_analysis\data\chats\LiangFan/txt/'

    # list_of_all_words = folder_to_list_of_words(foldername)

    # detect_and_count_multiple_entry_words(list_of_all_words)

    # list_of_unique_words = create_list_of_unique_words(list_of_all_words)
    # output_words_to_file(list_of_unique_words, 'D:\Chinese_vocabulary_analysis/data/all_unique_words.txt')
    filename = 'D:\Chinese_vocabulary_analysis\data\HSK5/all_unique_words_with_tones.txt'
    list_of_all_words = file_to_list_of_words(filename)
    print_words_by_character_with_frequencies(list_of_all_words, lowest_frequency=10)