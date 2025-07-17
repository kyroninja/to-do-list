# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for demo (in production, use a database)
todos = []

# Language mappings
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'nl': 'Dutch'
}

# Simple translation dictionary (in production, use Google Translate API)
TRANSLATIONS = {
    'es': {
        'buy groceries': 'comprar comestibles',
        'study': 'estudiar',
        'exercise': 'hacer ejercicio',
        'work': 'trabajar',
        'meeting': 'reunión',
        'call': 'llamar',
        'email': 'correo electrónico',
        'read': 'leer',
        'write': 'escribir',
        'clean': 'limpiar',
        'cook': 'cocinar',
        'sleep': 'dormir',
        'walk': 'caminar',
        'learn': 'aprender',
        'finish': 'terminar',
        'start': 'comenzar',
        'complete': 'completar',
        'review': 'revisar',
        'prepare': 'preparar',
        'organize': 'organizar'
    },
    'fr': {
        'buy groceries': 'acheter des produits alimentaires',
        'study': 'étudier',
        'exercise': 'faire de l\'exercice',
        'work': 'travailler',
        'meeting': 'réunion',
        'call': 'appeler',
        'email': 'email',
        'read': 'lire',
        'write': 'écrire',
        'clean': 'nettoyer',
        'cook': 'cuisiner',
        'sleep': 'dormir',
        'walk': 'marcher',
        'learn': 'apprendre',
        'finish': 'terminer',
        'start': 'commencer',
        'complete': 'compléter',
        'review': 'réviser',
        'prepare': 'préparer',
        'organize': 'organiser'
    },
    'de': {
        'buy groceries': 'Lebensmittel einkaufen',
        'study': 'studieren',
        'exercise': 'trainieren',
        'work': 'arbeiten',
        'meeting': 'Besprechung',
        'call': 'anrufen',
        'email': 'E-Mail',
        'read': 'lesen',
        'write': 'schreiben',
        'clean': 'putzen',
        'cook': 'kochen',
        'sleep': 'schlafen',
        'walk': 'gehen',
        'learn': 'lernen',
        'finish': 'beenden',
        'start': 'beginnen',
        'complete': 'abschließen',
        'review': 'überprüfen',
        'prepare': 'vorbereiten',
        'organize': 'organisieren'
    }
}

def get_next_id():
    """Generate next ID for new todo"""
    return max([todo['id'] for todo in todos], default=0) + 1

def translate_text(text, target_lang):
    """Simple translation function"""
    if target_lang not in TRANSLATIONS:
        return f"[{target_lang.upper()}] {text}"
    
    text_lower = text.lower()
    translation_dict = TRANSLATIONS[target_lang]
    
    # Check for exact matches first
    if text_lower in translation_dict:
        return translation_dict[text_lower]
    
    # Check for partial matches
    for english, translated in translation_dict.items():
        if english in text_lower:
            return text_lower.replace(english, translated)
    
    # Fallback
    return f"[{target_lang.upper()}] {text}"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', languages=LANGUAGES)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    """Add a new todo"""
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    todo = {
        'id': get_next_id(),
        'text': text,
        'completed': False,
        'created_at': datetime.now().isoformat(),
        'translation': None,
        'target_language': None
    }
    
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    data = request.get_json()
    
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    if 'completed' in data:
        todo['completed'] = data['completed']
    
    if 'text' in data:
        todo['text'] = data['text']
    
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'})

@app.route('/api/todos/<int:todo_id>/translate', methods=['POST'])
def translate_todo(todo_id):
    """Translate a todo"""
    data = request.get_json()
    target_lang = data.get('language')
    
    if not target_lang or target_lang not in LANGUAGES:
        return jsonify({'error': 'Invalid language'}), 400
    
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    # Translate the text
    translation = translate_text(todo['text'], target_lang)
    
    # Update the todo
    todo['translation'] = translation
    todo['target_language'] = LANGUAGES[target_lang]
    
    return jsonify(todo)

@app.route('/api/stats')
def get_stats():
    """Get todo statistics"""
    total = len(todos)
    completed = sum(1 for todo in todos if todo['completed'])
    pending = total - completed
    
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)