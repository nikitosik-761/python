
print("Введите кол-во рейтингов обучающихся: (rating_count)")
rating_count = int(input())

print("Введите значения рейтингов: (ratings)")
ratings = set(map(int, input().split()))

if len(ratings) != rating_count:
    raise ValueError(f"Введенный rating_count: [{rating_count}] не соответствует кол-ву ratings: [{len(ratings)}]")

sorted_ratings = sorted(ratings, reverse=True)

print(sorted_ratings[:2])
