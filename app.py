from flask import Flask, render_template, request, jsonify
from intelligent_text_engine import EnhancedIntelligentEngine

app = Flask(__name__)
engine = EnhancedIntelligentEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Process input
    engine.add_words_from_sentence(user_input)
    
    # helper for list formatting
    def format_list(l):
        return ", ".join(l) if l else "None"

    # Gather stats
    common_words = engine.get_common_words(n=3)
    last_word = user_input.split()[-1] if user_input.split() else ""
    suggestions = engine.search_prefix(last_word)
    next_word = engine.predict_next_word(last_word)
    related_words = engine.get_related_words(last_word)
    
    response_data = {
        'top_words': format_list(common_words),
        'last_word': last_word,
        'suggestions': format_list(suggestions),
        'next_word': next_word if next_word else "None",
        'related_words': format_list(related_words)
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
