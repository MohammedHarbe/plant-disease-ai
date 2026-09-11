"""
Fake AI Assistant for plant disease questions.

This module will eventually simulate an AI assistant that answers questions
about detected plant diseases, provides treatment recommendations, and 
offers prevention strategies.

ARCHITECTURE:
- This is a subsystem independent of FastAPI
- FastAPI will later import and call functions from this module
- The actual assistant implementation logic goes here
"""


def answer_question(question: str, context: dict = None) -> str:
    """
    Placeholder for assistant question-answering function.
    
    Eventually this will:
    - Accept a question about plant health/disease
    - Use context from previous predictions (optional)
    - Generate an intelligent response
    - Return guidance on treatment or prevention
    
    Args:
        question (str): User's question about plant health
        context (dict, optional): Context from disease detection (e.g., detected disease)
        
    Returns:
        str: Assistant response (to be implemented)
        
    TODO: Implement question-answering logic (can use LLM, rules-based, or hybrid)
    """
    raise NotImplementedError("AI Assistant not yet implemented")
