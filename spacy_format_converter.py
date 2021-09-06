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

nlp = spacy.blank("en")
# Create a blank Tokenizer with just the English vocab
msg = Printer()

SYMM_LABELS = ["Binds"]
MAP_LABELS = {
    "ROLE": "ROLE",
    "ADDRESS": "ADDRESS"
}

ann = "/content/sample.txt"
train_file='./relations_training.spacy'
dev_file='./relations_dev.spacy'
test_file='./relations_test.spacy'
def convert_to_binary(json_loc: Path, train_file: Path, dev_file: Path, test_file: Path):
  Doc.set_extension("rel", default={},force=True)
  vocab = Vocab()

  docs = {"train": [], "dev": [], "test": [], "total": []}
  ids = {"train": set(), "dev": set(), "test": set(), "total":set()}
  count_all = {"train": 0, "dev": 0, "test": 0,"total": 0}
  count_pos = {"train": 0, "dev": 0, "test": 0,"total": 0}

  with open(json_loc) as jsonfile:
      file = json.load(jsonfile)
      for example in file:
          span_starts = set()
          neg = 0
          pos = 0
          # Parse the tokens
          
          data = example["data"]
          annotation = example["annotations"]
          
          
          tokens=nlp(data["text"])
            

          spaces=[]
          spaces = [True if tok.whitespace_ else False for tok in tokens]
          words = [t.text for t in tokens]
          doc = Doc(nlp.vocab, words=words, spaces=spaces)

          # print(annotation[0]["result"])
          # Parse the GGP entities
          spans = annotation[0]["result"]
          entities = []
          span_end_to_start = {}
          # print(spans)
          for span in spans:
              
              if "value" in span.keys():
                # print(span["value"]["start"],span["value"]["end"])
                entity = doc.char_span(
                      int(span["value"]["start"]), 
                      int(span["value"]["end"]),
                      label = str(span["value"]["labels"][0])
                  )


                span_end_to_start[span["id"]] = span["id"]
                # print(span_end_to_start)
                entities.append(entity)
                span_starts.add(span["id"])

          doc.ents = entities
          # print(doc.ents)

          # Parse the relations
          rels = {}
          for x1 in span_starts:
              for x2 in span_starts:
                  rels[(x1, x2)] = {}
          # print(rels)

          #print(len(relations))
          for relation in spans:
            if "from_id" in relation.keys():
              # the 'head' and 'child' annotations refer to the end token in the span
              # but we want the first token
              start = span_end_to_start[relation["from_id"]]
              end = span_end_to_start[relation["to_id"]]
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

          # The annotation is complete, so fill in zero's where the data is missing
          for x1 in span_starts:
              for x2 in span_starts:
                  for label in MAP_LABELS.values():
                      if label not in rels[(x1, x2)]:
                          neg += 1
                          rels[(x1, x2)][label] = 0.0

                          #print(rels[(x1, x2)])
          doc._.rel = rels
          # print(doc._.rel)

          # only keeping documents with at least 1 positive case
          if pos > 0:
                  docs["total"].append(doc)
                  count_pos["total"] += pos
                  count_all["total"] += pos + neg

                  
                  
  print(len(docs["total"]))
  print(docs["total"])
  docbin = DocBin(docs = docs["total"], store_user_data=True)
  docbin.to_disk(train_file)
  msg.info(
      f"{len(docs['total'])} training sentences"
  )



