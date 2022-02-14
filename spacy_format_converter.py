import json
import random
import typer
from pathlib import Path
import pandas as pd
from spacy.tokens import Span, DocBin, Doc
from spacy.vocab import Vocab
from wasabi import Printer
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.util import compile_infix_regex
import re
import spacy
from spacy import displacy

from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
# tokenizer = Tokenizer(nlp.vocab,token_match=re.compile(r'\S+').match)
# tokens = tokenizer(text)
prefix_re = re.compile(r'''^[\?\<\>\-\@\*\%\!\[\+\=\#\}\{\_\$\/\\\\)\(]''')
# prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
# suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
suffix_re = re.compile(r'''[\?\<\>\-\@\*\%\!\+\[\=\#\}\{\_\/\.\,\$\\\]\)\(]''')
infix_re = re.compile(r'''[\?\:\;\~\<\>\-\=\#\}\{\_\/\$\\\"\'\)\(]''')
# prefix_re = compile_prefix_regex(final_list_prefixes)
# suffix_re = compile_suffix_regex(final_list_suffixes)

def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=None)
nlp = spacy.blank("en")
nlp.add_pipe('sentencizer')
nlp.tokenizer = custom_tokenizer(nlp)
sw_spacy = nlp.Defaults.stop_words
# nlp.add_pipe('dbpedia_spotlight', config={'confidence': 0.4, 'overwrite_ents':False})
# tokenizer = Tokenizer(nlp.vocab)
# nlp.tokenizer = Tokenizer(nlp.vocab,token_match=re.compile(r'\S+').match)
# Create a blank Tokenizer with just the English vocab
msg = Printer()

SYMM_LABELS = ["Binds"]
MAP_LABELS = {"ROLE": "ROLE",
              "ADDRESS": "ADDRESS",
              "IDCODE":"IDCODE",
              "PHRASE_RELATION":"PHRASE_RELATION"
}

ann = "/content/test_file.json"
train_file='./tarz_200_test.spacy'
dev_file='./relations_dev.spacy'
test_file='./relations_train.spacy'
# def main(json_loc: Path, train_file: Path, dev_file: Path, test_file: Path):
Doc.set_extension("rel", default={},force=True)
vocab = Vocab()

docs = {"train": [], "dev": [], "test": [], "total": []}
ids = {"train": set(), "dev": set(), "test": set(), "total":set()}
count_all = {"train": 0, "dev": 0, "test": 0,"total": 0}
count_pos = {"train": 0, "dev": 0, "test": 0,"total": 0}

for annotation_file in ["data/tarz_200_test.json"]:
    with open(f"./{annotation_file}") as jsonfile:
        file = json.load(jsonfile)
        count = 0
        for example in file:
            span_starts = set()
            main_doc_index= {}
            neg = 0
            pos = 0
            # Parse the tokens
            try:
                data = example["data"]
                annotation = example["annotations"]
                spans = annotation[0]["result"]
                list_labels = [span["value"]["text"] for span in spans if "value" in span.keys()]
    #                 print(list_labels)
                print(data["text"])
                text = data["text"]
                print("OLD len-->", len(old_text))
                # words = [word for word in old_text.split() if word.lower() not in sw_spacy]
                # text = " ".join(words)
                # print("New len-->", len(text))
                tokens=nlp(text)
                token_start_char = {tok.text :tok.idx for tok in tokens}
        #         print(token_start_char)
                token_end_char = {tok.text :tok.idx + len(tok.text) for tok in tokens}
                main_doc_index= {token.text : token.i for token in tokens}
                # print("MAIN_DOC_INDEX--> ", main_doc_index)




                space=[]
                spaces = [True if tok.whitespace_ else False for tok in tokens]
                words = [t.text for t in tokens]
                doc = Doc(nlp.vocab, words=words, spaces=spaces)

                entities = []
                span_end_to_start = {}
                id_token = {}
                start_span_token = {}
                end_span_token = {}
                annotated_word = [span["value"]["text"] for span in spans if "value" in span.keys()]
                count_annotated_word = pd.Series(annotated_word).value_counts().to_dict()
                print(count_annotated_word)
                        # print(spans)
                for span in spans:



                    if "value" in span.keys():


    #                     span["value"]["text"] =re.sub(pattern="[\“\”\"]",repl="",string = span["value"]["text"])
    #                     print("Span Value Text -->",span["value"]["text"])
    #                     print("\n")
                        span_token=nlp(span["value"]["text"])
    #                     span_token=re.findall( r'\w+|[^\s.\w]',span["value"]["text"])
                        print("Span Token -->",span_token)
                        len_span_tokens = len(span_token)
                        if len_span_tokens > 1 :
                            # print("Span TOKEN TEXT LENGTH >1 --> ",span_token.text)
    #                         token_start = main_doc_index[span_token[0]]
                            span_token_text = span_token.text
                            token_start = main_doc_index[span_token[0].text]
                            token_end = main_doc_index[span_token[0].text] + len_span_tokens
                            start_span_token[span["value"]["text"] ] = token_start

                            find_entity = re.finditer(r'({})'.format(re.escape(span_token.text)), text) ## <---
                            entity_start_end = [(match.group(),(match.start(), match.end()))for match in find_entity]
                            number_of_times_annotated_word_present = count_annotated_word[span_token.text]
                            for value in entity_start_end[:number_of_times_annotated_word_present]:

                                char_start = value[1][0]
                                char_end = value[1][1]
                                # print(char_start,char_end)
                                # for t in tokens:
                                #     if t.text == span_token.text
                                # char_start = span_token.text
                                # char_end = token_start_char[span_token.text] + len(span_token.text)
                                # print(char_start,char_end)
                                entity = doc.char_span(
                                  char_start, 
                                  char_end,
                                  label = span["value"]["labels"][0])
                                print(char_start,char_end)
                                # match = re.search(r'({})'.format(span["value"]["text"]), data["text"]) 
                                # char_start = match.start()
                                # char_end = match.end()

        #                         entity = doc.char_span(
        #                           char_start, 
        #                           char_end,
        #                           label = span["value"]["labels"][0])
        #                         print(char_start,char_end)


                                span_end_to_start[token_start] = token_start
                                id_token[span["id"]] = span["value"]["text"] 
                                print("Entity--> ",entity)
                                print("Label---> ", span["value"]["labels"][0])
                                entities.append(entity)
                                span_starts.add(token_start)


        #                     print(token_start,token_end)
                        else:
                            print("Span TOKEN TEXT length <1  --> ",span_token.text)


                            token_start = main_doc_index[span_token[0].text]
                            token_end = main_doc_index[span_token[0].text]
                            start_span_token[span["value"]["text"]] = token_start

                            find_entity = re.finditer(r'({})'.format(re.escape(span_token.text)), text) ## <---
                            entity_start_end = [(match.group(),(match.start(), match.end()))for match in find_entity]
                            number_of_times_annotated_word_present = count_annotated_word[span_token.text]
                            for value in entity_start_end[:number_of_times_annotated_word_present]:

                                char_start = value[1][0]
                                char_end = value[1][1]
                            # char_start = token_start_char[span_token.text]
                            # char_end = token_start_char[span_token.text] + len(span_token.text)
                                entity = doc.char_span(
                                      char_start, 
                                      char_end,
                                      label = span["value"]["labels"][0])
                                # print(char_start,char_end)
        #                         token_start = main_doc_index[span_token[0]]
        #                         start_span_token[span["value"]["text"] ] = token_start
        #                         match = re.search(r'({})'.format(span["value"]["text"]), data["text"]) 
        #                         char_start = match.start()
        #                         char_end = match.end()

        #                         entity = doc.char_span(
        #                           char_start, 
        #                           char_end,
        #                           label = span["value"]["labels"][0])
        #                         print(char_start,char_end)


                                span_end_to_start[token_start] = token_start
                                id_token[span["id"]] = span["value"]["text"]
                                print("Entity--> ",entity)
                                print("Label---> ", span["value"]["labels"][0])
                                entities.append(entity)
                                span_starts.add(token_start)
            #                 except:
            #                      pass




                # print(entities)
                # print("ID_to_TOEKN----> ", id_token)
                # try:
                # ent_not_in_doc_ents=[]
                # for en in list(doc.ents):
                #     if en not in entities:
                #         ent_not_in_doc_ents.append(en)
                doc.ents = entities
                #doc.ents = list(set(list(doc.ents)+entities))

                print(list(doc.ents))
                # except:
                #     pass

            #         except Exception:
            #              pass
                    # print(doc.ents)
                    # print(span_starts)
                    # print(id_token)
                # print(start_span_token)

                # Parse the relations
                rels = {}
                for x1 in span_starts:
                    for x2 in span_starts:
                        rels[(x1, x2)] = {}
                # print(rels)

            #print(len(relations))
                # try:
                for relation in spans:
                    if "from_id" in relation.keys():
                      # the 'head' and 'child' annotations refer to the end token in the span
                      # but we want the first token
                        start =start_span_token[id_token[relation["from_id"]]]
                        print(id_token[relation["from_id"]])
                        print("Relation_ID--->",relation["from_id"])
                        print("Start---> ",start)
                        end= start_span_token[id_token[relation["to_id"]]]
                        print(id_token[relation["to_id"]])               
                        print("Relation_to_ID--->",relation["to_id"])
                        print("End---> ", end)
                      # start = span_end_to_start[relation["from_id"]]
                      # end = span_end_to_start[relation["to_id"]]
                        label = relation["labels"][0]
                      #print(rels[(start, end)])
                        print(label)
                      #label = MAP_LABELS[label]
                      # print(start,end)
                        if label not in rels[(start, end)]:
                            rels[(start, end)][label] = 1.0
                            pos += 1
                          #print(pos)
                          #print(rels[(start, end)])
    #                 except:
    #                     pass

        #         else:
                # The annotation is complete, so fill in zero's where the data is missing
                for x1 in span_starts:
                    for x2 in span_starts:
                        for label in MAP_LABELS.values():
                            if label not in rels[(x1, x2)]:
                                neg += 1
                                rels[(x1, x2)][label] = 0.0

                                #print(rels[(x1, x2)])
                doc._.rel = rels
        #         print("DOCUMENT RELATIONS --> ",doc._.rel)

                # only keeping documents with at least 1 positive case
                if pos > 0:
                        docs["total"].append(doc)
                        count_pos["total"] += pos
                        count_all["total"] += pos + neg

                displacy.render(doc, style='ent', jupyter=True,)        
            except:
                pass
            count +=1

# print(len(docs["total"]))
# print("DOCS INSIDE --> ",docs["total"])
docbin = DocBin(docs = docs["total"], store_user_data=True)
docbin.to_disk(train_file)
msg.info(
    f"{count} Total sentences"
) 

msg.info(
    f"{len(docs['total'])} training sentences got converted to spacy format"
)
