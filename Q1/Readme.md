# Unigram Inverted Index

In the given problem statement, we were supposed to implement the unigram inverted index data structure on the given dataset. 


Provide support for the following commands:
```bash
  - x OR y
  - x AND y
  - x AND NOT y
  - x OR NOT y
```

Preprocessing used : 
```bash
   - Removal of stop words.
   - Removal of Block words(These are hand annotated).
   - Tokenization.
   - Lemmatization.
   - Tokens with less than length 2 are not considered.
```
      
The queries can be of more than 2 words of the form: "x OP1 y OP2 z" where OP1, OP2 = AND, OR, NOT.

Given a query, the model outputs : 
      
```bash     
  - the number of docs retrieved
  - the minimum number of total comparisons done (if any)
  - the list of documents retrieved.
```

