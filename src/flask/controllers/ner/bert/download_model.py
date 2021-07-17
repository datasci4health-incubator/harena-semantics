from biobert_pytorch import Ner
from transformers import ( BertForTokenClassification, BertTokenizer, AutoConfig )

MODEL_PATH = 'fagner/envoy'

print('Language Model:', MODEL_PATH)
# model = Ner(MODEL_PATH)
# print(model)
# output = model.predict(text)

tokenizer = BertTokenizer.from_pretrained(MODEL_PATH, do_lower_case=False)
config = AutoConfig.from_pretrained(MODEL_PATH)

labels = [value for k, value in config.id2label.items()]

model = BertForTokenClassification.from_pretrained(MODEL_PATH,
    num_labels=len(labels),
    output_attentions = False,
    output_hidden_states = False
)
