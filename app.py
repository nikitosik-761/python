from datetime import datetime
from fields import User, Product, Order


def show(items):
    if not items:
        print("(пусто)")
    for item in items:
        print(item)


def user_menu():
    print("---Пользователи---")
    print("1. Создать")
    print("2. Все")
    print("3. Найти по id")
    choice = input("Выбор: ").strip()

    if choice == "1":

        print("Введите имя: ")
        name = input()

        print("Введите email: ")
        email = input()

        print("Введите возвраст: ")
        age = int(input())

        print("Введите дату регистрации Y-%m-%d: ")
        registration_date = datetime.strptime(input(), "%Y-%m-%d").date()

        user = User(
            username=name,
            email=email,
            age=age,
            registration_date=registration_date,
        )
        user.save()

    elif choice == "2":
        show(User.all())

    elif choice == "3":
        print("Введите id для поиска")
        search_id = input()
        print(User.load(search_id))
    else:
        raise ValueError("Неверный выбор")


def product_menu():
    print("---Товары---")
    print("1. Создать")
    print("2. Все")
    print("3. Найти по id")
    choice = input("Выбор: ").strip()

    if choice == "1":

        print("Введите название продукта:")
        product_name = input()

        print("Введите цену")
        price = int(input())

        print("Введите кол-во")
        quantity = int(input())

        print("Введите категорию")
        category = input()

        product = Product(
            name=product_name,
            price=price,
            quantity=quantity,
            category=category,
        )
        product.save()

    elif choice == "2":
        show(Product.all())
    elif choice == "3":
        print("Введите id для поиска")
        search_id = input()
        print(Product.load(search_id))
    else:
        raise ValueError("Неверный выбор")


def order_menu():
    print("--- Заказы ---")
    print("1. Создать")
    print("2. Все")
    print("3. Найти по id")
    choice = input("Выбор: ").strip()

    if choice == "1":

        print("Введите id пользователя")
        user_id = input()

        print("Введите id продукта")
        product_id = input()

        print("Введите кол-во")
        quantity = int(input())

        print("Введите дату")
        order_date = datetime.strptime(input(), "%Y-%m-%d").date()

        print("Введите статус (ТОЛЬКО ЛАТИНСКИЕ):")
        status = input()

        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            order_date=order_date,
            status=status,
        )
        order.save()

    elif choice == "2":
        show(Order.all())
    elif choice == "3":
        print("Введите id для поиска")
        search_id = input()
        print(Order.load(search_id))
    else:
        raise ValueError("Неверный выбор")


def main():
    while True:
        print("1. Пользователи")
        print("2. Товары")
        print("3. Заказы")
        print("0. Выход")
        choice = input("Выбор: ").strip()

        if choice == "0":
            print("Выход")
            return
        elif choice == "1":
            user_menu()
        elif choice == "2":
            product_menu()
        elif choice == "3":
            order_menu()
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    main()
