# ArmTokenizer
Tokenizer for Armenian Language

## Usage
```python
#import Tokenizer
>>> from tokenizer import Tokenizer
>>> line = "Խուզարկությամբ հայտնաբերվեց տնկված 208 հատ, մինչ 4մ բարձրության կանեփի թուփ:"
>>> tokenizer = Tokenizer()
>>> tokenizer.tokenize(line)
>>> tokenizer.tokens()

['Խուզարկությամբ', 'հայտնաբերվեց', 'տնկված', '208', 'հատ', ',', 'մինչ', '4', 'մ', 'բարձրության', 'կանեփի', 'թուփ', ':']

```
