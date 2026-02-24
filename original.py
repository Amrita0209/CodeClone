def find_maximum(numbers):
    if not numbers:
        return None
    
    max_value = numbers[0]
    for num in numbers:
        if num > max_value:
            max_value = num
    return max_value

def calculate_average(data):
    total = 0
    count = 0
    for item in data:
        total += item
        count += 1
    return total / count if count > 0 else 0

class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades
    
    def get_gpa(self):
        if len(self.grades) == 0:
            return 0.0
        return sum(self.grades) / len(self.grades)