import sqlite3


def create_tables_and_insert_data():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
    ''')

    countries = [
        ('Казахстан',),
        ('Россия',),
        ('Германия',)
    ]

    cursor.executemany('INSERT INTO countries (title) VALUES (?)', countries)
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        area REAL DEFAULT 0,
        country_id INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    )
    ''')

    cities = [
        ('Алматы', 324.8, 1),
        ('Нур-Султан', 722, 1),
        ('Москва', 2561, 2),
        ('Санкт-Петербург', 1439, 2),
        ('Берлин', 891.8, 3),
        ('Мюнхен', 310.7, 3),
        ('Франкфурт', 248.3, 3)
    ]

    cursor.executemany('INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)', cities)
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        city_id INTEGER,
        FOREIGN KEY (city_id) REFERENCES cities(id)
    )
    ''')

    students = [
        ('Нурлан', 'Сабуров', 1),
        ('Петр', 'Ситников', 2),
        ('Кирилл', 'Баранов', 3),
        ('Виталий', 'Козловский', 4),
        ('Фридрих', 'Майер', 5),
        ('Лара', 'Фишер', 6),
        ('Луиза', 'Реммер', 7),
        ('Алина', 'Токтобекова', 1),
        ('Мария', 'Маркова', 2),
        ('Екатерина', 'Копейкина', 3),
        ('Владимир', 'Больших', 4),
        ('Хэнс', 'Вагнер', 5),
        ('Урсула', 'Шульц', 6),
        ('Клаудия', 'Веббер', 7),
        ('Ержан', 'Керимбеков', 1)
    ]

    cursor.executemany('INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)', students)
    conn.commit()

    conn.close()


def get_cities():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM cities')
    cities = cursor.fetchall()
    conn.close()
    return cities


def get_students_by_city(city_id):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    query = '''
    SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area
    FROM students
    JOIN cities ON students.city_id = cities.id
    JOIN countries ON cities.country_id = countries.id
    WHERE cities.id = ?
    '''
    cursor.execute(query, (city_id,))
    students = cursor.fetchall()
    conn.close()
    return students


def main():
    create_tables_and_insert_data()

    print(
        "Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")

    cities = get_cities()
    for city in cities:
        print(f"{city[0]}. {city[1]}")

    while True:
        try:
            city_id = int(input("Введите id города: "))
            if city_id == 0:
                break

            students = get_students_by_city(city_id)
            if students:
                for student in students:
                    print(
                        f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: {student[2]}, Город: {student[3]}, Площадь города: {student[4]}")
            else:
                print("В этом городе нет учеников.")
        except ValueError:
            print("Пожалуйста, введите корректный id города.")


if __name__ == "__main__":
    main()
