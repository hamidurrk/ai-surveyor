from enum import Enum, auto

class SurveyState(Enum):
    INTRODUCTION = auto()
    CONSENT = auto()
    QUESTIONING = auto()
    FOLLOW_UP = auto()
    COMPLETION = auto()

class StateMachine:
    def __init__(self, questions):
        self.state = SurveyState.INTRODUCTION
        self.questions = questions
        self.current_question = 0
        self.retry_count = 0
        self.max_retries = 2

    def transition(self, user_input):
        if self.state == SurveyState.INTRODUCTION:
            self.state = SurveyState.CONSENT
        elif self.state == SurveyState.CONSENT:
            if self._validate_consent(user_input):
                self.state = SurveyState.QUESTIONING
        elif self.state == SurveyState.QUESTIONING:
            if self._validate_answer(user_input):
                self.current_question += 1
                if self.current_question >= len(self.questions):
                    self.state = SurveyState.COMPLETION
            else:
                self.retry_count += 1
                self.state = SurveyState.FOLLOW_UP
        elif self.state == SurveyState.FOLLOW_UP:
            if self.retry_count < self.max_retries:
                self.state = SurveyState.QUESTIONING
            else:
                self.current_question += 1
                self.state = SurveyState.QUESTIONING
        return self.state

    def _validate_consent(self, response):
        return "agree" in response.lower()

    def _validate_answer(self, response):
        return len(response.strip()) > 5  # Basic validation