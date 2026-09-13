print("Введите кол-во операций:")
operations_count = int(input())

print("Введите первоначальный список:")
result = eval(input())

print("Введите команды:")
for _ in range(operations_count):
    parts = input().split()
    command, args = parts[0], parts[1:]

    match command:
        case "insert":
            result.insert(int(args[0]), int(args[1]))
        case "remove":
            result.remove(int(args[0]))
        case "append":
            result.append(int(args[0]))
        case "sort":
            result.sort()
        case "pop":
            result.pop()
        case "reverse":
            result.reverse()
        case "print":
            print(result)
        case _:
            raise ValueError(f"Неизвестная команда: [{command}]")
