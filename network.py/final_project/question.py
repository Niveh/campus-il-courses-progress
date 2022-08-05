class Question:
    def __init__(self, q_id, question, answers) -> None:
        self._id = q_id
        self._question = question
        self._answers = answers

    def get_id(self):
        return self._id

    def get_question(self):
        return self._question

    def get_answers(self):
        return self._answers

    def print_answers(self):
        for i, option in enumerate(self._answers):
            print(f"{i + 1}: {option}")

    def print_question(self):
        print(f"Q: {self._question}")

    def __str__(self):
        final = f"Q: {self._question}"
        for i, option in enumerate(self._answers):
            final += f"\n{i + 1}: {option}"

        return final
