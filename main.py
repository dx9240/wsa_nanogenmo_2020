from utilities import create_input_corpus, train_model, table_of_contents_builder, novel_generator, text_formatter, \
    novel_length, novel_version_maker

input_corpus = create_input_corpus('festival_input_texts')
textmodel = train_model(input_corpus)

# gets a tuple containing (generted text as list, number of chapters)
generated_text = novel_generator(textmodel, 2000)
# build the body of the novel
novel_body = text_formatter(generated_text[0])
length = novel_length(novel_body)

# create table of contents
table_of_contents = table_of_contents_builder(generated_text[1])
table_of_contents = text_formatter(table_of_contents)

novel_version_maker("generated_novel", 1, length, table_of_contents, novel_body)
