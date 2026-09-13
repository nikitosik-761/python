
BAD_GRADES = {0, 2}

print("Введите кол-во студетов и кол-во допустимых долгов")
student_count, allowed_debt_count = map(int, input().split())

students = {}

print("Введите идентификатор стдуента и список его оценок:")
for _ in range(student_count):
    parts = input().split()
    student_id_part_index = 0
    student_id = parts[student_id_part_index]

    grades = list(map(int, parts[1:]))
    students[student_id] = grades

expelled_students = []

for student_id, grades in students.items():
    debts = sum(1 for grade in grades if grade in BAD_GRADES)
    if debts > allowed_debt_count:
        expelled_students.append(student_id)

expelled_students.sort()

print("Идентификаторы студентов для отчисления:")
for student_id in expelled_students:
    print(student_id)