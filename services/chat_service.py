from rag.answer_generator import generate_answer

class ChatService:
    def respond(self, message: str, context: dict = None):
        return generate_answer(message)
