"""
Flask REST API for Communication Skills Scoring
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from rubric_parser import RubricParser
from scoring_engine import ScoringEngine
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize parser and scoring engine
print("Initializing rubric parser...")
parser = RubricParser()
rubrics = parser.get_rubrics()

print("Initializing scoring engine...")
scorer = ScoringEngine(rubrics)
print("API ready!")

@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        "message": "Communication Skills Scoring API",
        "version": "1.0",
        "endpoints": {
            "/api/score": "POST - Score a transcript",
            "/api/rubrics": "GET - Get rubrics",
            "/api/sample": "GET - Get sample transcript"
        }
    })

@app.route('/api/score', methods=['POST'])
def score_transcript():
    """
    Score a transcript
    Request body:
    {
        "transcript": "text to score",
        "duration_seconds": 60 (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'transcript' not in data:
            return jsonify({
                "error": "Missing transcript in request body"
            }), 400
        
        transcript = data['transcript'].strip()
        
        if not transcript:
            return jsonify({
                "error": "Transcript cannot be empty"
            }), 400
        
        duration_seconds = data.get('duration_seconds', None)
        
        # Score the transcript
        results = scorer.calculate_score(transcript, duration_seconds)
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({
            "error": f"Error scoring transcript: {str(e)}"
        }), 500

@app.route('/api/rubrics', methods=['GET'])
def get_rubrics():
    """Get the rubrics structure"""
    return jsonify(rubrics), 200

@app.route('/api/sample', methods=['GET'])
def get_sample():
    """Get sample transcript"""
    sample = parser.get_sample_transcript()
    return jsonify({
        "transcript": sample,
        "description": "Sample self-introduction transcript"
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    print("\n" + "="*80)
    print("Starting Communication Skills Scoring API...")
    print("API will be available at: http://localhost:5000")
    print("="*80 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
