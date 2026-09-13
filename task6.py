print("Введите строку:")
input_string = input()

if not input_string:
    raise ValueError("Строка не может быть пустой")

result = []

prev = input_string[0]
count = 1

for current_char in input_string[1:]:
    if current_char == prev:
        count += 1
    else:
        result.append((count, prev))
        prev = current_char
        count = 1

result.append((count, prev))

separator = " "

print(separator.join(f"({k}, {c})" for k, c in result))
