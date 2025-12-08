from collections import defaultdict, Counter
import networkx as nx

# Trie Data Structure for Auto-Completion
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._autocomplete(prefix, node)

    def _autocomplete(self, prefix, node):
        results = []
        if node.is_end_of_word:
            results.append(prefix)
        for char, next_node in node.children.items():
            results.extend(self._autocomplete(prefix + char, next_node))
        return results

# Bigram Model for Predicting Next Words
class BigramModel:
    def __init__(self):
        self.bigram_counts = defaultdict(Counter)
    
    def add_sentence(self, words):
        for i in range(len(words) - 1):
            self.bigram_counts[words[i]][words[i + 1]] += 1
    
    def predict_next_word(self, current_word):
        if current_word in self.bigram_counts:
            return self.bigram_counts[current_word].most_common(1)[0][0]
        return None

# Red-Black Tree Node
class RBTreeNode:
    def __init__(self, word, color="red"):
        self.word = word
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

# Red-Black Tree for Word Storage
class RedBlackTree:
    def __init__(self):
        self.TNULL = RBTreeNode(None, color="black")
        self.root = self.TNULL

    def insert(self, word):
        # Simple Red-Black Tree insertion (pseudo-balanced for this demonstration)
        new_node = RBTreeNode(word)
        new_node.left = self.TNULL
        new_node.right = self.TNULL
        new_node.parent = None
        self._insert_node(new_node)

    def _insert_node(self, node):
        # Insert the node into the tree and balance (basic structure for example)
        y = None
        x = self.root
        while x != self.TNULL:
            y = x
            if node.word < x.word:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.word < y.word:
            y.left = node
        else:
            y.right = node
        node.color = "red"  # Simplified for example

    def search(self, word):
        return self._search_tree_helper(self.root, word)

    def _search_tree_helper(self, node, word):
        if node == self.TNULL or word == node.word:
            return node.word if node != self.TNULL else None
        if word < node.word:
            return self._search_tree_helper(node.left, word)
        return self._search_tree_helper(node.right, word)

# Graph-Based Word Relationships
class WordGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_relationship(self, word1, word2):
        if self.graph.has_edge(word1, word2):
            self.graph[word1][word2]['weight'] += 1
        else:
            self.graph.add_edge(word1, word2, weight=1)

    def find_related_words(self, word):
        if word in self.graph:
            return list(self.graph.successors(word))
        return []

# Combined Intelligent Engine with Red-Black Tree and Graph
class EnhancedIntelligentEngine:
    def __init__(self):
        self.trie = Trie()
        self.red_black_tree = RedBlackTree()
        self.word_graph = WordGraph()
        self.word_frequency = Counter()
        self.bigram_model = BigramModel()

    def add_words_from_sentence(self, sentence):
        words = sentence.split()
        for word in words:
            self.word_frequency[word] += 1
            self.trie.insert(word)
            self.red_black_tree.insert(word)
        
        for i in range(len(words) - 1):
            self.word_graph.add_relationship(words[i], words[i + 1])

        self.bigram_model.add_sentence(words)
    
    def get_common_words(self, n=3):
        return [word for word, _ in self.word_frequency.most_common(n)]
    
    def search_prefix(self, prefix):
        return self.trie.search(prefix)
    
    def predict_next_word(self, current_word):
        return self.bigram_model.predict_next_word(current_word)
    
    def search_word(self, word):
        return self.red_black_tree.search(word)
    
    def get_related_words(self, word):
        return self.word_graph.find_related_words(word)

# Main Program
if __name__ == "__main__":
    print("================================================")
    print("    Welcome to the AI Conversational Agent!    ")
    print("================================================\n")
    
    engine = EnhancedIntelligentEngine()
    conversation_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("\nThank you for using the chatbot. Goodbye!")
            break

        conversation_history.append(user_input)
        engine.add_words_from_sentence(user_input)

        # Display the output in an organized format
        print("\n--- Chatbot Response ---")
        common_words = engine.get_common_words(n=3)
        print("📈 Top Words:", ", ".join(common_words) if common_words else "None")

        last_word = user_input.split()[-1] if user_input.split() else ""
        suggestions = engine.search_prefix(last_word)
        print(f"🔍 Suggestions for '{last_word}':", ", ".join(suggestions) if suggestions else "None")

        next_word = engine.predict_next_word(last_word)
        print("📝 Next Word Prediction:", next_word if next_word else "None")

        related_words = engine.get_related_words(last_word)
        print("🔗 Related Words:", ", ".join(related_words) if related_words else "None")
        print("--- End of Response ---\n")