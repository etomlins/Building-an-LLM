# From chapter 2: Working with text data
import re

# consists of 
# splitting text into words
# 
# converting words into tokens
# 
# turning tokens into embedding vectors.

# (1) Pull short story "The Verdict"
import urllib.request
url = ("https://raw.githubusercontent.com/rasbt/"
       "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
       "the-verdict.txt")
file_path = "the-verdict.txt"
urllib.request.urlretrieve(url, file_path)

with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
print("Total number of character:", len(raw_text))
print(raw_text[:99])

# (2) Split text into words
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
print(preprocessed[:30])

print(len(preprocessed))

# (3) Create vocabulary
# each word is mapped to a unique integer
all_words = sorted(set(preprocessed))
vocab_size = len(all_words)
print(vocab_size)

vocab = {token:integer for integer,token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break

# then, convert new text into token ids 
class SimpleTokenizerV1:
    def __init__(self, vocab):
        #1 Stores the vocabulary as a class attribute for access in the encode and decode methods
        self.str_to_int = vocab
        #2 Creates an inverse vocabulary that maps token IDs back to the original text tokens
        self.int_to_str = {i:s for s,i in vocab.items()}

    def encode(self, text):
        #3 Processes input text into token IDs
        preprocessed = re.split(r'([,.?_!"()\']|--|\s)', text)
        preprocessed = [
            item.strip() for item in preprocessed if item.strip()
        ]
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids

    def decode(self, ids):
        #4 Converts token IDs back into text
        text = " ".join([self.int_to_str[i] for i in ids]) 
        
        # 5 Removes spaces before the specified punctuation
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)    #5
        return text

tokenizer = SimpleTokenizerV1(vocab)
text = """"It's the last he painted, you know," 
       Mrs. Gisburn said with pardonable pride."""
ids = tokenizer.encode(text)
print(ids)
print(tokenizer.decode(ids))

all_tokens = sorted(list(set(preprocessed)))
all_tokens.extend(["<|endoftext|>", "<|unk|>"])
vocab = {token:integer for integer,token in enumerate(all_tokens)}

print(len(vocab.items()))
