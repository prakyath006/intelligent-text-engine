This project is an experimental AI-powered conversational engine that analyzes user input in real time using multiple classic data structures and models. Instead of generating replies, it focuses on understanding and organizing the text you type, then showing intelligent insights like common words, auto-complete suggestions, next-word predictions, and related terms.

Core Components & Data Structures

Trie (Prefix Tree) – Auto-completion
A Trie is used to store all words from the conversation.
It supports fast prefix search and is used to suggest possible completions for the last word the user types.

Bigram Model – Next-word prediction
A simple bigram language model tracks how often each word is followed by another.
Using this, the engine predicts the most likely next word based on the current word.

Red-Black Tree – Word storage & lookup
A (simplified) Red-Black Tree structure is used to store words in sorted order and support efficient search.
This demonstrates how self-balancing BST-style structures can be used for dictionary-like word lookup.

Directed Word Graph – Word relationships
A directed graph (using NetworkX) is used to represent relationships between consecutive words as edges.
From this, the engine can fetch words that commonly follow a given word, showing local context and associations.

Word Frequency Counter – Top word statistics
A Counter is maintained to track how often each word appears.
This is used to display the most common words in the conversation so far.

How It Works (Runtime Flow)

User enters a sentence in the console.

The sentence is split into words and:

Inserted into the Trie

Inserted into the Red-Black Tree

Counted in the frequency counter

Added to the bigram model and word graph as consecutive pairs

The engine then prints:

The top N most frequent words

Auto-complete suggestions for the last word

A predicted next word based on bigrams

Related words from the graph that typically follow the last word

This project showcases how combining classic data structures (Trie, Red-Black Tree, Graph) with simple NLP ideas (bigrams, word frequencies) can build an “intelligent” backend for conversational analysis and typing assistance.
