def get_max(items):
    if not items:
        return None
    
    biggest = items[0]
    for x in items:
        if x > biggest:
            biggest = x
    return biggest

def compute_mean(values):
    sum_total = 0
    counter = 0
    for val in values:
        sum_total += val
        counter += 1
    return sum_total / counter if counter > 0 else 0

class Pupil:
    def __init__(self, student_name, scores):
        self.student_name = student_name
        self.scores = scores
    
    def calculate_grade_point(self):
        if len(self.scores) == 0:
            return 0.0
        return sum(self.scores) / len(self.scores)