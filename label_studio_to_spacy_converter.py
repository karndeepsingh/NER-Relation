import json

import typer
from pathlib import Path

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
prefix_re = re.compile(r'''^[\[\(]''')
# prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
# suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
suffix_re = re.compile(r'''[\.\,\]\)]''')
infix_re = re.compile(r'''[\?\:\;\~]''')

def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=None)
nlp = spacy.blank("en")
nlp.tokenizer = custom_tokenizer(nlp)
# nlp.add_pipe('dbpedia_spotlight', config={'confidence': 0.4, 'overwrite_ents':False})
# tokenizer = Tokenizer(nlp.vocab)
# nlp.tokenizer = Tokenizer(nlp.vocab,token_match=re.compile(r'\S+').match)
# Create a blank Tokenizer with just the English vocab
msg = Printer()

SYMM_LABELS = ["Binds"]
MAP_LABELS = {"PARTY NAME":"PARTY NAME",
              "IDCODE":"IDCODE",
    "ROLE": "ROLE",
    "ADDRESS": "ADDRESS"
}

ann = "/content/test_file.json"
train_file='./relations_test.spacy'
dev_file='./relations_dev.spacy'
test_file='./relations_train.spacy'
# def main(json_loc: Path, train_file: Path, dev_file: Path, test_file: Path):
Doc.set_extension("rel", default={},force=True)
vocab = Vocab()

docs = {"train": [], "dev": [], "test": [], "total": []}
ids = {"train": set(), "dev": set(), "test": set(), "total":set()}
count_all = {"train": 0, "dev": 0, "test": 0,"total": 0}
count_pos = {"train": 0, "dev": 0, "test": 0,"total": 0}

with open("./test_file.json") as jsonfile:
    file = json.load(jsonfile)
    for example in file:
        span_starts = set()
        neg = 0
        pos = 0
        # Parse the tokens
#         try:
        data = example["data"]
        annotation = example["annotations"]
        spans = annotation[0]["result"]
        list_labels = [span["value"]["text"] for span in spans if "value" in span.keys()]
        print(list_labels)

#         try:
# #         b_l_t = ['"borrower"', '"lender"', '"trustee"']
#             for label in list_labels:
#                     data["text"] = re.sub(r'({})'.format(label),label.upper(),data["text"])
#         except:
#             pass
#         else:    
#         data["text"] = re.sub(pattern="[\“\”\"]",repl="",string=data["text"])
        print(data["text"])
        tokens=nlp(data["text"])
        token_start_char = {tok.text :tok.idx for tok in tokens}
#         print(token_start_char)
        token_end_char = {tok.text :tok.idx + len(tok.text) for tok in tokens}
        main_doc_index= {token.text : token.i for token in tokens}
#         data["text"]
#         res = re.findall( r'\w+|[^\s.\w]', data["text"])
#         main_doc_index = {ent:i for i, ent in enumerate(res)}
#         print("MAIN DOC INDEX ---> ", main_doc_index)




        spaces=[]
        spaces = [True if tok.whitespace_ else False for tok in tokens]
        words = [t.text for t in tokens]
        doc = Doc(nlp.vocab, words=words, spaces=spaces)

        # print(annotation[0]["result"])
        # Parse the GGP entities
        spans = annotation[0]["result"]
        entities = []
        span_end_to_start = {}
        id_token = {}
        start_span_token = {}
        end_span_token = {}
            # print(spans)
        try:
            for span in spans:



                if "value" in span.keys():


#                     span["value"]["text"] =re.sub(pattern="[\“\”\"]",repl="",string = span["value"]["text"])
                    span_token=nlp(span["value"]["text"])
#                     span_token=re.findall( r'\w+|[^\s.\w]',span["value"]["text"])
#                     print(span_token)
                    len_span_tokens = len(span_token)
                    if len_span_tokens > 1 :
                        print("Span TOKEN TEXT LENGTH >1 --> ",span_token.text)
#                         token_start = main_doc_index[span_token[0]]

                        token_start = main_doc_index[span_token[0].text]
                        token_end = main_doc_index[span_token[0].text] + len_span_tokens
                        start_span_token[span["value"]["text"] ] = token_start

                        match = re.search(r'({})'.format(span_token.text), data["text"]) 
                        char_start = match.start()
                        char_end = match.end()

                        entity = doc.char_span(
                          char_start, 
                          char_end,
                          label = span["value"]["labels"][0])
                        print(char_start,char_end)
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


    #                     print(token_start,token_end)
                    else:
                        print("Span TOKEN TEXT length <1  --> ",span_token.text)


                        token_start = main_doc_index[span_token[0].text]
                        token_end = main_doc_index[span_token[0].text]
                        start_span_token[span["value"]["text"]] = token_start

                        match = re.search(r'({})'.format(span_token.text), data["text"]) 
                        char_start = match.start()
                        char_end = match.end()
                        entity = doc.char_span(
                              char_start, 
                              char_end,
                              label = span["value"]["labels"][0])
                        print(char_start,char_end)
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
        except:
             pass




        print(entities)
        print("ID_to_TOEKN----> ", id_token)
        try:
            doc.ents = entities
        except:
            pass

    #         except Exception:
    #              pass
            # print(doc.ents)
            # print(span_starts)
            # print(id_token)
        print(start_span_token)

        # Parse the relations
        rels = {}
        for x1 in span_starts:
            for x2 in span_starts:
                rels[(x1, x2)] = {}
        # print(rels)

    #print(len(relations))
        try:
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
                  #print(label)
                  #label = MAP_LABELS[label]
                  # print(start,end)
                    if label not in rels[(start, end)]:
                        rels[(start, end)][label] = 1.0
                        pos += 1
                      #print(pos)
                      #print(rels[(start, end)])
        except:
            pass

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
#         except:
#             pass

# print(len(docs["total"]))
# print("DOCS INSIDE --> ",docs["total"])
docbin = DocBin(docs = docs["total"], store_user_data=True)
docbin.to_disk(train_file)
msg.info(
    f"{len(docs['total'])} training sentences"
)   