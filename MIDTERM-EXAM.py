import panda as pd
import numpy as np


class InvalidScoreError(Exception):
    pass

class StudentRecordLockedError(Exception):
    pass

class Student:
    def __init__(self, name, scores):
        self.name = name.strip()
        self.scores = np.array([])
        self.locked = False
        for score in scores:
            self._add(float(score))
    
    def _add(self, score):
        if not (0 <= score <= 100):
            raise InvalidScoreError(f"Score {score} not in 0-100")
        self.scores = np.append(self.scores, score)
    
    def lock(self):
        self.locked = True
    
    def add_score(self, score):
        if self.locked:
            raise StudentRecordLockedError(f"Cannot add to {self.name}")
        self._add(float(score))
    
    def average(self):
        return np.mean(self.scores)
    
    def __str__(self):
        return f"{self.name} — {self.average():.2f} avg."

def process_quiz_data(raw_rows):
    df = pd.DataFrame(raw_rows)
    df['name'] = df['name'].str.strip()
    df = df.drop_duplicates(subset=['name'], keep='first')
    
    students, failures = [], []
    for row in df.to_dict('records'):
        try:
            students.append(Student(row['name'], row['scores'].split(',')))
        except Exception as e:
            failures.append({"row": row, "error": str(e)})
    return students, failures

if __name__ == "__main__":
    raw_rows = [
        {"name": " Amara ", "scores": "92,85,78"},
        {"name": "Leo", "scores": "88,91,73"},
        {"name": "Priya", "scores": "65,72,150"},
        {"name": "Sam", "scores": "70,not_a_number,60"},
        {"name": "Amara", "scores": "95,90,88"},
        {"name": "Jade", "scores": "81,77,84,90"},
    ]
    
    students, failures = process_quiz_data(raw_rows)
    
    print("=== Students ===")
    for s in students:
        print(s)
    
        print("\n=== Failed Rows ===")
    for f in failures:
        print(f"Skipped: {f['row']} -> {f['error']}")
    
    print("\n=== Lock Demo ===")
    demo = Student("Demo", [85, 90])
    demo.lock()
    try:
        demo.add_score(95)
    except StudentRecordLockedError as e:
        print(f"Exception: {e}")
    
    print("\n=== Ranked ===")
    for i, s in enumerate(sorted(students, key=lambda s: s.average(), reverse=True), 1):
        print(f"{i}. {s}")