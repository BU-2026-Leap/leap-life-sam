from contracts import DataProcessor, ExamScore

class ExamDataProcessor(DataProcessor):

    def compute_number_of_unique_students(self, scores: [ExamScore]) -> int:
        """
        Given a list of ExamScore's, computes the number of unique students in the data set
        """

        # TODO: implement here
        student_set = set()
        for score in scores:
            student_set.add(score.student_id)
        return len(student_set)

    def compute_average_final(self, scores: [ExamScore]) -> float:
        """
        Given a list of ExamScore's, computes the average of all final scores
        """

        # TODO: implement here
        total_scores = 0.0
        final_count = 0
        for score in scores:
            if score.exam_name == "final":
                total_scores = total_scores + score.score
                final_count += 1
        if final_count == 0:
            return 0
        return total_scores / final_count
