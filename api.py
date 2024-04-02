from flask import Flask, request, jsonify
from agents import FactsGenerator
app = Flask(__name__)

# Placeholder for storing submitted question and documents
question_and_documents = {}
facts = FactsGenerator()
# Placeholder for storing computed facts
computed_facts = {}


@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    global question_and_documents
    data = request.json
    question = data.get('question')
    documents = data.get('documents')
    auto_approve = data.get('autoApprove', False)

    # Logic to process submitted question and documents
    # This could involve indexing documents, extracting facts, and suggesting changes

    # Storing submitted question and documents
    question_and_documents = {
        'question': question,
        'documents': documents,
        'auto_approve': auto_approve
    }

    return '', 200


@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    global question_and_documents
    if not question_and_documents:
        return jsonify({'message': 'No question and documents submitted.'}), 404

    question = question_and_documents.get('question')

    computed_facts = facts.query_index(question)
    # If facts are still being computed
    if not computed_facts:
        return jsonify({'question': question, 'status': 'processing'}), 200

    # If facts are computed
    return jsonify({'question': question, 'factsByDay': computed_facts, 'status': 'done'}), 200


if __name__ == '__main__':
    app.run(debug=True)
