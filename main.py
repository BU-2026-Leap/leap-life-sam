import csv
import os
import json
from pathlib import Path

full_base_path = Path(__file__).resolve().parent
input_filename = full_base_path / "test_scores.csv"
output_filename = "output.json"

if os.path.exists(output_filename):
    os.remove(output_filename)

#average_final = 0.0
#unique_students = 0
#total_scores = 0
#final_count = 0
#student_set = set()

def compute_avg_final_score(file):
    total_scores = 0
    final_count = 0
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)
            if row["exam_name"] == "final":
                total_scores = total_scores + float(row["score"])
                final_count = final_count + 1
    return (total_scores / final_count)

def count_unique_students(file):
    student_set = set()
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            student_set.add(row["student_id"])
        return len(student_set)

def print_results(file):
    print("The average final score is " + str(compute_avg_final_score(file)))
    print("The number of unique students in the data set is " + str(count_unique_students(file)))

#with open(input_filename) as f:
 #   reader = csv.DictReader(f)
  #  for row in reader:
   #     print(row)

        # TODO: compute average final score

#        if row["exam_name"] == "final":
 #           total_scores = total_scores + float(row["score"])
  #          final_count = final_count + 1
        # TODO: unique student count
   #     student_set.add(row["student_id"])
    #    unique_students = len(student_set)


    #average_final = (total_scores / final_count)
average_final = compute_avg_final_score(input_filename)
print(average_final)
unique_students = count_unique_students(input_filename)
print(unique_students)

print_results(input_filename)

if os.path.exists(output_filename):
    os.remove(output_filename)

result = {
    "average_final": average_final,
    "unique_students": unique_students,
}

with open(output_filename, "w") as out:
    json.dump(result, out, indent=2)

