# Treaty text cleanup 
# Remove non english words
# Clean up characters and non-word items
import re 
import nltk
nltk.download('words')
words = set(nltk.corpus.words.words())

# Remove non-english using NLTK

test = '''
Note by the SecretariatandRegulations to give effect to Article 102of the 
Charter of the United Nations,adopted by the General Assembly on 
14 December Traitds ou accords internationaux transmis par un 
Membrtde 'Organisation des Nations Unies et conclus avant la date.
'''

test = re.findall('[A-Z][^A-Z]*', test)
test = ' '.join(test)
test = " ".join(w for w in nltk.wordpunct_tokenize(test) if w.lower() in words or not w.isalpha())
