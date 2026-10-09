from app.schemas.chat import ChatResponse


class BootstrapService:
    """
    Service layer for bootstrap chat functionality.
    This is a local implementation that provides simple responses
    without integrating any LLM provider.
    """

    def __init__(self):
        self.provider = "bootstrap-local"

    def process_question(self, question: str) -> ChatResponse:
        """
        Process a user question and return a bootstrap response.

        Args:
            question: The user's question

        Returns:
            ChatResponse with answer and provider information
        """
        # Simple bootstrap logic - returns a predefined response
        # In a real implementation, this would connect to an LLM
        answer = self._generate_answer(question)
        return ChatResponse(answer=answer, provider=self.provider)

    def _generate_answer(self, question: str) -> str:
        """
        Generate a simple answer based on the question.
        This is a placeholder implementation.
        """
        # Normalize the question for simple matching
        question_lower = question.lower()

        # Simple keyword-based responses
        if "fastapi" in question_lower:
            return "FastAPI es un framework web moderno y de alto rendimiento para construir APIs con Python 3.7+ basado en type hints estándar de Python."
        elif "python" in question_lower:
            return "Python es un lenguaje de programación de alto nivel, interpretado y multiparadigma conocido por su legibilidad y simplicidad."
        elif "api" in question_lower:
            return "Una API (Application Programming Interface) es un conjunto de reglas y protocolos que permite que diferentes aplicaciones se comuniquen entre sí."
        elif "llm" in question_lower or "modelo de lenguaje" in question_lower:
            return "Los Modelos de Lenguaje Grande (LLM) son sistemas de IA entrenados con grandes cantidades de texto para comprender y generar lenguaje humano."
        else:
            return f"Esta es una respuesta de bootstrap para la pregunta: '{question}'. Esta es una implementación local de demostración sin integración con un LLM real."
