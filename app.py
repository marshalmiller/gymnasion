#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gymnasion Web App
Interactive literary training web application based on the original Gymnasion CLI tool.
"""

from flask import Flask, render_template, request, jsonify, session
import json
import random
import os
from datetime import datetime
import uuid

# Simplified version that doesn't require all the heavy ML dependencies
# This creates a working web app with mock responses for demonstration

app = Flask(__name__)
app.secret_key = 'gymnasion_secret_key_' + str(uuid.uuid4())

# Mock data for demonstration (in a real deployment, you'd use the actual data files)
MOCK_ADJECTIVES = {
    "forest": ["dark", "ancient", "mysterious", "green", "dense"],
    "mountain": ["towering", "snow-capped", "rugged", "majestic", "distant"],
    "bird": ["soaring", "melodious", "swift", "graceful", "colorful"],
    "sea": ["vast", "turbulent", "azure", "endless", "foaming"],
    "default": ["beautiful", "strange", "wonderful", "terrible", "sublime"]
}

MOCK_VERBS = {
    "wolf": [("devour", "prey"), ("hunt", "deer"), ("howl", "moon")],
    "bird": [("sing", "song"), ("fly", "sky"), ("build", "nest")],
    "mountain": [("tower", "valley"), ("shelter", "village"), ("hold", "snow")],
    "default": [("love", "beauty"), ("seek", "truth"), ("create", "art")]
}

MOCK_QUOTES = [
    ("The mountains are calling and I must go.", "John Muir"),
    ("In every walk with nature, one receives far more than they seek.", "John Muir"),
    ("The sea, once it casts its spell, holds one in its net of wonder forever.", "Jacques Cousteau"),
    ("Look deep into nature, and then you will understand everything better.", "Albert Einstein"),
    ("The poetry of earth is never dead.", "John Keats")
]

MOCK_AUTHORS = ["dickinson", "whitman", "shakespeare", "yeats", "frost"]

class GymnasionWebApp:
    def __init__(self):
        pass
    
    def reset_session(self):
        """Reset session state"""
        session['poem_text'] = ""
        session['banished_words'] = []
        session['used_quotes'] = []
        session['boredom'] = 0
        session['to_imitate'] = ""
        session['imitation_attempts'] = 0
    
    def ensure_session(self):
        """Ensure session variables exist"""
        if 'poem_text' not in session:
            session['poem_text'] = ""
        if 'banished_words' not in session:
            session['banished_words'] = []
        if 'used_quotes' not in session:
            session['used_quotes'] = []
        if 'boredom' not in session:
            session['boredom'] = 0
        if 'to_imitate' not in session:
            session['to_imitate'] = ""
        if 'imitation_attempts' not in session:
            session['imitation_attempts'] = 0
    
    def analyze_text(self, text, mode='mixed'):
        """Main analysis function that returns gymnastic responses"""
        if not text.strip():
            return None
            
        # Ensure session variables exist
        self.ensure_session()
            
        # Add to poem
        session['poem_text'] += "\n" + text
        session['boredom'] += 1
        
        # Define response types by mode
        mode_functions = {
            'elaboration': [
                self._question_about_adjectives,
                self._question_about_verb,
                self._question_about_object,
                self._word2vec_suggestions,
                self._comment_about_entities
            ],
            'imitation': [
                self._suggest_quote,
                self._suggest_quote_stub,
                self._authorial_imitation
            ],
            'variation': [
                self._word_banishment,
                self._check_banished_words,
                self._repetition_judgment
            ],
            'backtracking': [
                self._command_recall_noun,
                self._command_comparison
            ],
            'mixed': [
                self._question_about_adjectives,
                self._question_about_verb,
                self._question_about_object,
                self._suggest_quote,
                self._word_banishment,
                self._check_banished_words,
                self._authorial_imitation,
                self._word2vec_suggestions,
                self._repetition_judgment,
                self._command_recall_noun,
                self._command_comparison
            ]
        }
        
        response_types = mode_functions.get(mode, mode_functions['mixed'])
        
        # Prioritize certain checks regardless of mode
        if session.get('banished_words'):
            banned_check = self._check_banished_words(text)
            if banned_check:
                return banned_check
                
        if session.get('to_imitate') and mode in ['imitation', 'mixed']:
            imitation_check = self._authorial_imitation(text)
            if imitation_check:
                return imitation_check
        
        # Try different response types based on mode
        random.shuffle(response_types)
        for response_func in response_types:
            try:
                response = response_func(text)
                if response:
                    return response
            except Exception:
                continue
                
        return "Continue..."
    
    def _extract_nouns(self, text):
        """Extract nouns from text (simplified)"""
        # Simple noun extraction - in real app would use SpaCy
        words = text.lower().split()
        # Common nouns for demo
        common_nouns = ["forest", "mountain", "bird", "sea", "tree", "sky", "sun", "moon", 
                       "star", "river", "lake", "flower", "stone", "wind", "fire", "earth",
                       "wolf", "deer", "eagle", "lion", "bear", "snake", "fish", "horse"]
        return [word for word in words if word in common_nouns]
    
    def _question_about_adjectives(self, text):
        """Ask about adjectives for nouns"""
        nouns = self._extract_nouns(text)
        if not nouns:
            return None
            
        noun = random.choice(nouns)
        adjectives = MOCK_ADJECTIVES.get(noun, MOCK_ADJECTIVES["default"])
        adj_sample = random.sample(adjectives, min(2, len(adjectives)))
        
        return f"What sort of {noun}? {adj_sample[0].title()}? {adj_sample[1].title() if len(adj_sample) > 1 else 'Beautiful'}?"
    
    def _question_about_verb(self, text):
        """Ask about verbs"""
        nouns = self._extract_nouns(text)
        if not nouns:
            return None
            
        noun = random.choice(nouns)
        verbs = MOCK_VERBS.get(noun, MOCK_VERBS["default"])
        verb, obj = random.choice(verbs)
        
        beginnings = ["What could", "Why does", "What shall", "What did", "Why would"]
        return f"{random.choice(beginnings)} the {noun} {verb}?"
    
    def _question_about_object(self, text):
        """Ask about objects"""
        nouns = self._extract_nouns(text)
        if not nouns:
            return None
            
        noun = random.choice(nouns)
        verbs = MOCK_VERBS.get(noun, MOCK_VERBS["default"])
        verb, obj = random.choice(verbs)
        
        beginnings = ["What could", "What does", "What shall", "What did"]
        return f"{random.choice(beginnings)} the {noun} do to the {obj}?"
    
    def _suggest_quote(self, text):
        """Suggest a relevant quote"""
        if session['used_quotes'] and len(session['used_quotes']) >= len(MOCK_QUOTES):
            session['used_quotes'] = []  # Reset if all used
            
        available_quotes = [q for q in MOCK_QUOTES if q not in session['used_quotes']]
        if not available_quotes:
            return None
            
        quote, author = random.choice(available_quotes)
        session['used_quotes'].append((quote, author))
        
        prefixes = ["Learn from this mastery", "Now imitate this", "Emulate this discourse", 
                   "Listen and respond", "Student, learn from these words"]
        
        return f"{random.choice(prefixes)}:\n\"{quote}\"\n   ({author})"
    
    def _word_banishment(self, text):
        """Banish a word"""
        nouns = self._extract_nouns(text)
        available_nouns = [n for n in nouns if n not in session['banished_words']]
        
        if not available_nouns:
            return None
            
        banned_word = random.choice(available_nouns)
        session['banished_words'].append(banned_word)
        
        rel_words = ["kin", "brethren", "kindred", "neighbors"]
        return f"I forbid you from singing of {banned_word} or this word's {random.choice(rel_words)}."
    
    def _check_banished_words(self, text):
        """Check if banished words are used"""
        if not session.get('banished_words'):
            return None
            
        words = text.lower().split()
        for word in words:
            if word in session['banished_words']:
                responses = ["Are you even paying attention to yourself?", 
                           "You forget my instructions.", "How narrow your mind...",
                           "How disappointing.", "Try harder."]
                return f"{random.choice(responses)}\nI said not to sing of {word}..."
        return None
    
    def _authorial_imitation(self, text):
        """Handle authorial imitation"""
        if not session.get('to_imitate'):
            # Start imitation
            author = random.choice(MOCK_AUTHORS)
            session['to_imitate'] = author
            session['imitation_attempts'] = 3
            return f"Try that again, in the style of {author.title()}."
        else:
            # Check imitation
            session['imitation_attempts'] -= 1
            if session['imitation_attempts'] <= 0 or random.random() < 0.3:  # Sometimes succeed
                response = random.choice(["Good.", "Satisfactory.", 
                                        "I hope you have learned by letting go of yourself."])
                session['to_imitate'] = ""
                session['imitation_attempts'] = 0
                return response
            else:
                return f"No, not that style --- imitate {session['to_imitate'].title()}."
    
    def _suggest_quote_stub(self, text):
        """Suggest a quote fragment to complete"""
        prefixes = ["Now finish this true sentence:", "Now follow this wordpath:",
                   "Let these words take you by the tongue:", "Follow me:",
                   "Complete these words:"]
        
        # Simple quote stubs for demo
        stubs = [
            "The mountains are calling and I must",
            "In every walk with nature, one receives",
            "Look deep into nature, and then you will",
            "The poetry of earth is never",
            "Two roads diverged in a yellow"
        ]
        
        stub = random.choice(stubs)
        return f"{random.choice(prefixes)}\n\"{stub}...\""
    
    def _comment_about_entities(self, text):
        """Comment on people and places"""
        # Simple entity detection - look for capitalized words
        words = text.split()
        entities = [word for word in words if word[0].isupper() and len(word) > 2]
        
        if not entities:
            return None
            
        entity = random.choice(entities)
        
        # Assume it's a person if common name, otherwise place
        person_questions = [
            f"Now sing in praise of {entity}...",
            f"Now sing me of the youth of {entity}...",
            f"Now sing to me what we may learn from the sins of {entity}..."
        ]
        
        place_questions = [
            f"Show me {entity}...the taste of the people, the customs...",
            f"Yes, now lure me to {entity}...",
            f"Now describe the history of {entity}..."
        ]
        
        # Simple heuristic - assume places if they end with common suffixes
        if entity.lower().endswith(('land', 'ton', 'ville', 'berg', 'burg')):
            return random.choice(place_questions)
        else:
            return random.choice(person_questions)
    
    def _word2vec_suggestions(self, text):
        """Suggest related words"""
        nouns = self._extract_nouns(text)
        if not nouns:
            return None
            
        noun = random.choice(nouns)
        # Mock related words
        related_words = {
            "forest": ["woodland", "grove", "thicket"],
            "mountain": ["peak", "summit", "ridge"],
            "bird": ["dove", "raven", "sparrow"],
            "sea": ["ocean", "waves", "tide"]
        }
        
        suggestions = related_words.get(noun, ["beauty", "truth", "wonder"])
        selected = random.sample(suggestions, min(2, len(suggestions)))
        
        response = f"You've sung me {noun}...now sing me "
        for word in selected:
            response += f"{word}..."
        return response
        """Suggest related words"""
        nouns = self._extract_nouns(text)
        if not nouns:
            return None
            
        noun = random.choice(nouns)
        # Mock related words
        related_words = {
            "forest": ["woodland", "grove", "thicket"],
            "mountain": ["peak", "summit", "ridge"],
            "bird": ["dove", "raven", "sparrow"],
            "sea": ["ocean", "waves", "tide"]
        }
        
        suggestions = related_words.get(noun, ["beauty", "truth", "wonder"])
        selected = random.sample(suggestions, min(2, len(suggestions)))
        
        response = f"You've sung me {noun}...now sing me "
        for word in selected:
            response += f"{word}..."
        return response
    
    def _repetition_judgment(self, text):
        """Comment on repetitive syntax"""
        if session['boredom'] < 3:
            return None
            
        words = text.split()
        if len(words) > 3 and words[0].lower() == "i":
            session['boredom'] = 0
            return "Eschew this tired syntax:\n   \"" + " ".join(words[:4]) + "...\""
        return None
    
    def _command_recall_noun(self, text):
        """Command to recall earlier noun"""
        if session['boredom'] < 5:
            return None
            
        # Extract nouns from poem history
        poem_words = session['poem_text'].split()
        nouns = [word for word in poem_words if word.lower() in 
                ["forest", "mountain", "bird", "sea", "tree", "sky", "sun", "moon"]]
        
        if not nouns:
            return None
            
        session['boredom'] = 0
        old_noun = random.choice(nouns)
        beginnings = ["I grow weary.", "I grow bored.", "You have lost the thread."]
        endings = ["Return to the part about the {}", "Tell me more about the {}"]
        
        return f"{random.choice(beginnings)} {random.choice(endings).format(old_noun)}."
    
    def _command_comparison(self, text):
        """Command comparison between nouns"""
        if session['boredom'] < 5:
            return None
            
        current_nouns = self._extract_nouns(text)
        poem_words = session['poem_text'].split()
        old_nouns = [word for word in poem_words if word.lower() in 
                    ["forest", "mountain", "bird", "sea", "tree", "sky"]]
        
        if not current_nouns or not old_nouns:
            return None
            
        session['boredom'] = 0
        current_noun = random.choice(current_nouns)
        old_noun = random.choice(old_nouns)
        
        questions = ["Which will last longer?", "Which is deeper?", "Which is more lovely?",
                    "Which is closer to the divine?", "Which is more virtuous?"]
        
        return f"Now compare the {old_noun} to the {current_noun}. {random.choice(questions)}"

# Initialize the app
gym_app = GymnasionWebApp()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze user input and return gymnastic response"""
    data = request.get_json()
    user_input = data.get('text', '').strip()
    mode = data.get('mode', 'mixed')
    
    if not user_input:
        return jsonify({'response': 'Please enter some text.'})
    
    response = gym_app.analyze_text(user_input, mode)
    
    return jsonify({
        'response': response or "Continue...",
        'banished_words': session.get('banished_words', []),
        'to_imitate': session.get('to_imitate', ''),
        'poem_length': len(session.get('poem_text', '').split()),
        'current_mode': mode
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the session"""
    session.clear()
    gym_app.reset_session()
    return jsonify({'status': 'reset'})

@app.route('/status')
def status():
    """Get current session status"""
    return jsonify({
        'banished_words': session.get('banished_words', []),
        'to_imitate': session.get('to_imitate', ''),
        'poem_length': len(session.get('poem_text', '').split()),
        'boredom': session.get('boredom', 0)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
