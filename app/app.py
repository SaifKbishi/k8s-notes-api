#app.py
from flask import Flask, jsonify, render_template, request
import json

print("hello world 00")

app = Flask(__name__)

@app.route('/')
def index():
    print("hello world 01")
    return "all good notes api is running (Health check)"
    #return render_template('index.html')

@app.route('/notes', methods=['GET'])
def get_notes():
    print("hello world 02")
    with open('notes.json', 'r') as f:
        notes = json.load(f)
    return jsonify(notes)

# Get a specific note by ID
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    with open('notes.json', 'r') as f:
        notes = json.load(f)
        note = next((note for note in notes if note['id'] == note_id), None)        
        if note:            
            return jsonify(note)
        else:
            return jsonify({"error": "Note not found"}), 404

@app.route('/addnote', methods=['POST'])
def add_note():
    new_note = request.get_json()
    with open('notes.json', 'r') as f:
        notes = json.load(f)
        notes.append(new_note)
        with open('notes.json', 'w') as f:
            json.dump(notes, f, indent=4)
    return jsonify(new_note), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200 

@app.route('/notes/data')
def get_data():    
    sample_data = {
        "name": "Flask App",
        "version": "1.0",
        "status": "Running"
    }
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000, debug=True) 