import csv
import os
import json

input_filename = "test_scores.csv"
output_filename = "output.json"

if os.path.exists(output_filename):
    os.remove(output_filename)

average_final = 0.0
unique_students = 0
total_scores = 0
final_count = 0

with open(input_filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

        # TODO: compute average final score

        if row["exam_name"] == "final":
            total_scores = total_scores + float(row["score"])
            final_count = final_count + 1
        # TODO: unique student count

    unique_students = final_count
    average_final = (total_scores / unique_students)


if os.path.exists(output_filename):
    os.remove(output_filename)

result = {
    "average_final": average_final,
    "unique_students": unique_students,
}

with open(output_filename, "w") as out:
    json.dump(result, out, indent=2)

