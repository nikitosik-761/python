
print("Введите кол-во рейтингов обучающихся: (rating_count)")
rating_count = int(input())

students = {}

print("Введите данные студентов")
for _ in range(rating_count):
    student_id, student_rating = input().split(";")
    students.update({student_id: int(student_rating)})

top_two_ratings = sorted(set(students.values()), reverse=True)[:2]

print("Топ студентов:")
for s_id, s_rating in students.items():
    if s_rating in top_two_ratings:
        print(s_id)

