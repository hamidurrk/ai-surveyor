from agents import QuestionGenerator
from PyPDF2 import PdfReader

class AdminConsole:
    def __init__(self):
        self.question_gen = QuestionGenerator()
    
    def create_survey(self):
        source_type = input("Enter input type (pdf/prompt): ").lower()
        
        if source_type == 'pdf':
            questions = self._handle_pdf_input()
        elif source_type == 'prompt':
            questions = self._handle_prompt_input()
        else:
            print("Invalid input type")
            return None
        
        if questions and self._get_approval(questions):
            return questions
        return None
    
    def _handle_pdf_input(self):
        path = input("Enter PDF path: ")
        try:
            text = self._extract_pdf_text(path)
            return self.question_gen.generate_from_pdf(text)
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None
    
    def _handle_prompt_input(self):
        prompt = input("Enter your survey topic prompt: ")
        return self.question_gen.generate_from_prompt(prompt)
    
    def _extract_pdf_text(self, path):
        reader = PdfReader(path)
        return " ".join([page.extract_text() for page in reader.pages])
    
    def _get_approval(self, questions):
        print("\nGenerated Questions:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")
        return input("\nApprove these questions? (y/n): ").lower() == 'y'