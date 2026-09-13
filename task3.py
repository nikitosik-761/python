print("Введите кол-во рейтингов обучающихся: (rating_count)")
rating_count = int(input())

students = []

print("Введите обучающихся и их оценки:")
for _ in range(rating_count):
    parts = input().split()
    student_id_part_index = 0
    student_id = parts[student_id_part_index]

    grades = list(map(int, parts[1:]))
    average_grade = sum(grades) / len(grades)

    students.append((student_id, average_grade))

students.sort(key=lambda item: item[1], reverse=True)

print("Итого:")
for student_id, average_grade in students:
    print(f"{student_id} {average_grade:.2f}")
