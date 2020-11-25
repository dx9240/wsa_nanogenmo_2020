import glob
import os
from os.path import join
import markovify
from nltk import word_tokenize


def create_input_corpus(directory_name):
    """ Function to combine all the files in a directory into one txt file"""
    directory_path = join(os.getcwd(), directory_name, '*.txt')
    corpus = []
    for file_path in glob.iglob(directory_path):
        with open(file_path) as file:
            file_text = file.read()
            corpus.append(file_text)
    return corpus


def train_model(input_corpus):
    '''
    Function to train markovify model
    '''
    textmodel = markovify.Text(' '.join(input_corpus))

    return textmodel


def table_of_contents_builder(chapter_size):
    table_contents = ['Table of Contents\n\nIntroduction\n']
    chapter_counter = 1
    for chapter in range(chapter_size):
        line = f"Chapter {chapter_counter}\n"
        table_contents.append(line)
        chapter_counter += 1
        # stop adding chapters when the number of chapters you generated has been reached
        if chapter_counter > chapter_size:
            break
    return table_contents


def novel_generator(textmodel, num_of_sentences, paragraph_size=6, chapter_size=20):
    '''function to generate novel based on markovify model given as first parameter,
    and number of sentences to generated given as second parameter. The optional
     parameters determine the sentence length of paragraphs and chapters. Returns a
     tuple.[0] contains a list of all generated sentences,[1] the number
     of chapters as an int'''

    # list for storing generated sentences
    novel_list = []
    # latex_list = []
    # counter to count sentences in order to know when to break a paragraph
    sentence_counter = 0
    paragraph_counter = 0
    chapter_counter = 0
    # if no chapter exists, create chapter 1
    if paragraph_counter == 0:
        chapter_counter += 1
        novel_list.append("Introduction\n\n")
        # latex_list.append("\\addcontentsline{toc}{section}{Chapter %}" % chapter_counter)
        # otherwise, start generating and counting sentences
        # generate number of sentences
        for i in range(num_of_sentences):
            output_text = textmodel.make_sentence()
            novel_list.append(output_text)
            sentence_counter += 1
            # if more than some number of sentences are appended, break the paragraph
            if sentence_counter == paragraph_size:
                novel_list.append('\n\n')
                sentence_counter = 0
                paragraph_counter += 1
            # if more than some number of paragraphs are created, break the chapter and create the next chapter
            if paragraph_counter == chapter_size:
                novel_list.append('\n\n')
                novel_list.append(f"Chapter {chapter_counter}\n\n")
                paragraph_counter = 0
                chapter_counter += 1

    return (novel_list, chapter_counter)


def text_formatter(text_list):
    # build list into a string
    text = ' '.join(text_list)
    return text


def novel_length(novel_text):
    novel_text = word_tokenize(novel_text)
    text_length = len(novel_text)
    message = (f"The novel is approximately {text_length} words long")
    return message


def novel_version_maker(file_name, version_number, length, table_of_contents, novel_body):
    with open(f'{file_name}_version_{version_number}.txt', 'w+') as file:
        file.write(length)
        file.write('\n')
        file.write(table_of_contents)
        file.write('\n')
        file.write(novel_body)

# TODO add book formatting
