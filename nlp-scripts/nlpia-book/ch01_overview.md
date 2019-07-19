---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.1.6
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

## A simple chatbot


### match greetings

```python
import re
```

```python
r = "(hi|hello|hey)[ ]*([a-z]*)"
re.match(r, 'Hello Rosa', flags=re.IGNORECASE)
```

```python
re.match(r, "hi ho, hi ho, it's off to work ...", flags=re.IGNORECASE)
```

```python
re.match(r, "hey, what's up", flags=re.IGNORECASE)
```

```python
r = r'''[^a-z]*([y]o|[h']?ello|ok|hey|(good[ ])?(morn[gin']{0,3}|afternoon|even[gin']{0,3}))[\s,;:]{1,3}([a-z]{1,20})'''
re_greeting = re.compile(r, flags=re.IGNORECASE)
```

```python
re_greeting.match('Hello Rosa')
```

```python
re_greeting.match('Hello Rosa').groups()
```

```python
re_greeting.match("Good morning Rosa")
```

```python
re_greeting.match("Good Manning Rosa")
```

```python
re_greeting.match('Good evening Rosa Parks').groups()
```

```python
re_greeting.match("Good Morn'n Rosa")
```

```python
re_greeting.match("yo Rosa")
```

### output generator

```python
my_names = set(['rosa', 'rose', 'chatty', 'chatbot', 'bot', 'chatterbot'])
curt_names = set(['hal', 'you', 'u'])
greeter_name = ''
match = re_greeting.match(input())
if match:
    at_name = match.groups()[-1]
    if at_name in curt_names:
        print("Good one.")
    elif at_name.lower() in my_names:
        print("Hi {}, How are you?".format(greeter_name))
```

### bag-of-word vectors

```python
from collections import Counter
```

```python
Counter("Guten Morgen Rosa".split())
```

```python
Counter("Good morning, Rosa!".split())
```

### word order and grammar

```python
from itertools import permutations
[" ".join(combo) for combo in permutations("Good morning Rosa!".split(), 3)]
```

```python
s = """Find textbooks with titles containing 'NLP', 
    or 'natural' and 'language', or 
    'computational' and  'linguistics'."""
len(set(s.split()))

```

```python
import numpy as np
np.arange(1, 12 + 1).prod()  # factorial(12) = arange(1, 13).prod()
```

```python

```
