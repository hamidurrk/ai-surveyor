import requests
import re
import json

class DialogueAgent:
    def __init__(self, model_name="deepseek-r1:1.5b"):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = model_name
    
    def generate_response(self, prompt_template, **kwargs):
        prompt = prompt_template.format(**kwargs)
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 256
            }
        }
        
        try:
            response = requests.post(
                self.ollama_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            return json.loads(response.text)["response"].strip()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {str(e)}")
            return "There was an error processing your request. Please try again."

class QuestionGenerator(DialogueAgent):
    def __init__(self):
        super().__init__()
    
    def generate_from_pdf(self, pdf_text):
        prompt = f"""Extract key survey questions from this text. 
        Return only a numbered list of questions ending with question marks:
        
        {pdf_text[:3000]}"""  # Truncate for context limit
        
        questions = super().generate_response(prompt)
        return self._parse_questions(questions)
    
    def generate_from_prompt(self, user_prompt):
        prompt = f"""Generate 5-10 survey questions based on this topic:
        {user_prompt}
        Return only a numbered list of questions ending with question marks:"""
        
        questions = super().generate_response(prompt)
        return self._parse_questions(questions)
    
    def _parse_questions(self, text):
        return re.findall(r'\d+[\.\)]\s*(.*?)\?', text)