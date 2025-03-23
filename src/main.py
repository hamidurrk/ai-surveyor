from database import Session, SurveySession
from state_machine import StateMachine, SurveyState
from agents import DialogueAgent, QuestionGenerator
import time

class SurveySystem:
    def __init__(self):
        self.dialogue_agent = DialogueAgent()
        self.db_session = Session()
        self.sessions = {}
        
    def start_survey(self, user_id, questions):
        state_machine = StateMachine(questions)
        session = SurveySession(
            session_id=user_id,
            questions=questions,
            state=state_machine.state.name
        )
        self.db_session.add(session)
        self.db_session.commit()
        return self._handle_state(user_id, state_machine)
    
    def _handle_state(self, user_id, state_machine):
        while True:
            if state_machine.state == SurveyState.INTRODUCTION:
                message = self._get_introduction()
            elif state_machine.state == SurveyState.CONSENT:
                message = self._get_consent_prompt()
            elif state_machine.state == SurveyState.QUESTIONING:
                message = self._get_question_prompt(state_machine)
            elif state_machine.state == SurveyState.FOLLOW_UP:
                message = self._get_followup_prompt(state_machine)
            elif state_machine.state == SurveyState.COMPLETION:
                return self._get_completion_message()
            
            user_response = input(f"System: {message}\nYou: ")
            new_state = state_machine.transition(user_response)
            self._update_session(user_id, new_state, user_response)
            
            if new_state == SurveyState.COMPLETION:
                break

    def _get_introduction(self):
        return self.dialogue_agent.generate_response(
            "Create a friendly survey introduction explaining we're collecting "
            "user feedback. Keep it under 3 sentences."
        )

    def _get_consent_prompt(self):
        return self.dialogue_agent.generate_response(
            "Politely ask for consent to proceed with the survey. "
            "Include option to agree/disagree."
        )

    def _get_question_prompt(self, state_machine):
        return self.dialogue_agent.generate_response(
            "Ask this survey question in a conversational way: {question}",
            question=state_machine.questions[state_machine.current_question]
        )

    def _get_followup_prompt(self, state_machine):
        return self.dialogue_agent.generate_response(
            "Rephrase this question to get better response. "
            "Add a helpful example: {question}",
            question=state_machine.questions[state_machine.current_question]
        )

    def _get_completion_message(self):
        return self.dialogue_agent.generate_response(
            "Create a warm survey completion message that thanks the user "
            "and explains how their data will be used."
        )

    def _update_session(self, user_id, new_state, response):
        session = self.db_session.query(SurveySession).filter_by(session_id=user_id).first()
        session.state = new_state.name
        session.responses = session.responses or []
        session.responses.append(response)
        self.db_session.commit()

if __name__ == "__main__":
    system = SurveySystem()
    questions = ["What is your age?", "What is your occupation?"]  # From admin module
    user_id = f"user_{int(time.time())}"
    print(system.start_survey(user_id, questions))