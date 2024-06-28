
import psycopg2
import random
from datetime import datetime, timedelta
import time
from transfer import materials_in_elasticsearch

conn  = psycopg2.connect(
    user="root",
    password="9967992",
    host="localhost",
    port="5433",
    database="postgres"  # Или другое имя базы данных, если она была создана
)



cur = conn.cursor()


def generate_UniMain():
    cur.execute(
        "INSERT INTO univmain (id, name) VALUES (%s, %s)",
        (1, 'MIREA')
    )


def generate_faculties():
    faculties = ['ИТ', 'ИКБСП']
    n = len (faculties)


    for i in range(n):
        cur.execute(
            "INSERT INTO univ (uni_id, name, unimain_id) VALUES (%s, %s, %s)",
            (i+1, faculties[i], 1)
        )

def generate_specialities():
    specialities = [ '09.03.02', '09.03.04']

    for i in range(len(specialities)):
        cur.execute(
            "INSERT INTO spec (spec_id, name, main_caf) VALUES (%s, %s, %s)",
            (i+1, specialities[i], i + 1)
        )

def generate_specialities_univ():

        for i in range(2):
            cur.execute(
                "INSERT INTO Univ_spec (spec_in_uni, spec_id, uni_id) VALUES (%s, %s, %s)",
                (i+1, i+1, i+1)
            )


def generate_cafedras():
    cafedras = ['КБ-2', 'КБ-3']

    for i in range(len(cafedras)):
        cur.execute(
            "INSERT INTO cafedra (cafedra_id,   name, uni_id) VALUES (%s, %s, %s)",
            (i+1, cafedras[i], i+1)
        )


def generate_courses():
    courses = ['Програмирование', 'Математика']
    courses_2 = ['Физика', 'Информатика']

    i = 0
    for course in courses:
        cur.execute(
            "INSERT INTO courses (course_id ,course_name, cafedra_id) VALUES (%s, %s, %s)",
            (i+1, course, 1)
        )

        cur.execute(
            "INSERT INTO courses_in_spec (spec_id, course_id) VALUES (%s, %s)",
            (1, i+1)
        )
        i += 1

    for course in courses_2:
        cur.execute(
            "INSERT INTO courses (course_id ,course_name, cafedra_id) VALUES (%s, %s, %s)",
            (i+1, course, 2)
        )

        cur.execute(
            "INSERT INTO courses_in_spec (spec_id, course_id) VALUES (%s, %s)",
            (2, i+1)
        )
        i += 1


def generate_lecturers():
    lectures = ['Основы программирования', 'Алгоритмы и структуры данных', 'Основы информатики', 'Основы компьютерных сетей', 'Основы баз данных', 'Основы теории информации', 'Основы теории вычислительных процессов', 'Основы теории алгоритмов']
    lectures_for_math = ['Основы математики', 'Алгебра', 'Геометрия', 'Математический анализ', 'Дискретная математика', 'Теория вероятностей', 'Математическая статистика', 'Математическая логика']
    lectures_for_phisics = ['Основы физики', 'Механика', 'Электродинамика', 'Термодинамика', 'Квантовая механика', 'Оптика', 'Атомная физика', 'Ядерная физика']
    lectures_for_informatics = ['Основы информатики', 'Алгоритмы и структуры данных', 'Основы программирования', 'Основы компьютерных сетей', 'Основы баз данных', 'Основы теории информации', 'Основы теории вычислительных процессов', 'Основы теории алгоритмов']

    materials_for_programig = [
        'В этой лекции мы рассмотрим основы программирования, включая типы данных, операторы, циклы, условия и функции. Мы также узнаем о различных языках программирования и их использовании.',
        'В этой лекции мы рассмотрим алгоритмы и структуры данных, которые являются фундаментальными понятиями в информатике. Мы узнаем о различных типах алгоритмов и структур данных, их свойствах и применении.',
        'В этой лекции мы рассмотрим основы информатики, включая основы вычислительных систем, теорию информации и искусственный интеллект. Мы узнаем о том, как работают компьютеры, как кодировать информацию и как создавать искусственный интеллект.',
        'В этой лекции мы рассмотрим основы компьютерных сетей, включая физические принципы передачи данных, сетевые протоколы и сетевые приложения. Мы узнаем о том, как компьютеры взаимодействуют друг с другом в сети.',
        'В этой лекции мы рассмотрим основы баз данных, включая структуру баз данных, операции с базами данных и языки запросов к базам данных. Мы узнаем о том, как хранить и обрабатывать данные в базе данных.',
        'В этой лекции мы рассмотрим основы теории информации, включая основные понятия, такие как энтропия, кодирование и декодирование. Мы узнаем о том, как измерять количество информации и как передавать информацию в условиях помех.',
        'В этой лекции мы рассмотрим основы теории вычислительных процессов, включая основные понятия, такие как сложность вычислений и алгоритмическая сложность. Мы узнаем о том, как оценивать сложность алгоритмов и как решать вычислительные задачи эффективно.',
        'В этой лекции мы рассмотрим основы теории алгоритмов, включая основные понятия, такие как алгоритмы, эффективность алгоритмов и алгоритмическая сложность. Мы узнаем о том, как анализировать алгоритмы и как разрабатывать эффективные алгоритмы.'
    ]
    materials_for_math = [
        'В этой лекции мы рассмотрим основы математики, включая основные понятия, такие как числа, операции и функции. Мы узнаем о том, как работать с числами и как решать математические задачи.',
        'В этой лекции мы рассмотрим алгебру, включая основные понятия, такие как алгебраические операции, алгебраические структуры и алгебраические системы. Мы узнаем о том, как решать алгебраические задачи.',
        'В этой лекции мы рассмотрим геометрию, включая основные понятия, такие как геометрические фигуры, геометрические преобразования и геометрические системы. Мы узнаем о том, как решать геометрические задачи.',
        'В этой лекции мы рассмотрим математический анализ, включая основные понятия, такие как функции, пределы и производные. Мы узнаем о том, как решать математические задачи с помощью математического анализа.',
        'В этой лекции мы рассмотрим дискретную математику, включая основные понятия, такие как дискретные структуры, дискретные преобразования и дискретные системы. Мы узнаем о том, как решать дискретные задачи.',
        'В этой лекции мы рассмотрим теорию вероятностей, включая основные понятия, такие как вероятностные пространства, вероятностные события и вероятностные распределения. Мы узнаем о том, как решать задачи теории вероятностей.',
        'В этой лекции мы рассмотрим математическую статистику, включая основные понятия, такие как выборка, статистические оценки и статистические гипотезы. Мы узнаем о том, как решать задачи математической статистики.',
        'В этой лекции мы рассмотрим математическую логику, включая основные понятия, такие как логические операции, логические структуры и логические системы. Мы узнаем о том, как решать задачи математической логики.'
    ]
    materials_for_phisics = [
        'В этой лекции мы рассмотрим основы физики, включая основные понятия, такие как механика, электродинамика, термодинамика и оптика. Мы узнаем о том, как работает мир вокруг нас.',
        'В этой лекции мы рассмотрим механику, включая основные понятия, такие как движение, сила, работа и энергия. Мы узнаем о том, как описывать и анализировать движение тел.',
        'В этой лекции мы рассмотрим электродинамику, включая основные понятия, такие как электричество, магнетизм, электромагнетизм и электроника. Мы узнаем о том, как работают электрические и магнитные поля.',
        'В этой лекции мы рассмотрим термодинамику, включая основные понятия, такие как теплота, температура, термодинамические процессы и термодинамические системы. Мы узнаем о том, как работают тепловые двигатели и холодильные машины.',
        'В этой лекции мы рассмотрим квантовую механику, включая основные понятия, такие как квантовые состояния, квантовые преобразования и квантовые системы. Мы узнаем о том, как работают квантовые процессы и квантовые устройства.',
        'В этой лекции мы рассмотрим оптику, включая основные понятия, такие как свет, зрение, оптические приборы и оптические системы. Мы узнаем о том, как работают оптические явления и оптические устройства.',
        'В этой лекции мы рассмотрим атомную физику, включая основные понятия, такие как атомы, молекулы, ядра и частицы. Мы узнаем о том, как работают атомные и молекулярные процессы.',
        'В этой лекции мы рассмотрим ядерную физику, включая основные понятия, такие как ядерные реакции, ядерные процессы и ядерные системы. Мы узнаем о том, как работают ядерные установки и ядерные реакторы.'
    ]
    materials_for_informatics = [
        'В этой лекции мы рассмотрим основы информатики, включая основные понятия, такие как информационные системы, информационные технологии и информационные процессы. Мы узнаем о том, как работают информационные системы и как их разрабатывать.',
        'В этой лекции мы рассмотрим алгоритмы и структуры данных, включая основные понятия, такие как алгоритмы, структуры данных и алгоритмические процессы. Мы узнаем о том, как работают алгоритмы и структуры данных.',
        'В этой лекции мы рассмотрим основы программирования, включая основные понятия, такие как языки программирования, программные системы и программные процессы. Мы узнаем о том, как работают программные системы и как их разрабатывать.',
        'В этой лекции мы рассмотрим основы компьютерных сетей, включая основные понятия, такие как сетевые технологии, сетевые системы и сетевые процессы. Мы узнаем о том, как работают компьютерные сети и как их разрабатывать.',
        'В этой лекции мы рассмотрим основы баз данных, включая основные понятия, такие как базы данных, базовые системы и базовые процессы. Мы узнаем о том, как работают базовые системы и как их разрабатывать.',
        'В этой лекции мы рассмотрим основы теории информации, включая основные понятия, такие как информационные процессы, информационные системы и информационные технологии. Мы узнаем о том, как работают информационные системы и как их разрабатывать.',
        'В этой лекции мы рассмотрим основы теории вычислительных процессов, включая основные понятия, такие как вычислительные процессы, вычислительные системы и вычислительные технологии. Мы узнаем о том, как работают вычислительные системы и как их разрабатывать.',
        'В этой лекции мы рассмотрим основы теории алгоритмов, включая основные понятия, такие как алгоритмы, алгоритмические процессы и алгоритмические технологии. Мы узнаем о том, как работают алгоритмические системы и как их разрабатывать.'
    ]



    i = 0
    for lecture in lectures:
        cur.execute(
            "INSERT INTO lectures (lecture_id, lecture_name, course_id) VALUES (%s, %s, %s)",
            (i+1, lecture, 1)
        )
        cur.execute(
            "INSERT INTO lectures_materials (material_id,lecture_id, content) VALUES (%s, %s, %s)",
            (i+1, i+1, materials_for_programig[i])
        )
        i += 1

    for lecture in lectures_for_math:
        cur.execute(
            "INSERT INTO lectures (lecture_id, lecture_name, course_id) VALUES (%s, %s, %s)",
            (i+1, lecture, 2)
        )
        cur.execute(
            "INSERT INTO lectures_materials (material_id , lecture_id, content) VALUES (%s, %s, %s)",
            (i+1, i+1, materials_for_math[i-8])
        )
        i += 1

    for lecture in lectures_for_phisics:
        cur.execute(
            "INSERT INTO lectures (lecture_id, lecture_name, course_id) VALUES (%s, %s, %s)",
            (i+1, lecture, 3)
        )
        cur.execute(
            "INSERT INTO lectures_materials (material_id , lecture_id, content) VALUES (%s, %s, %s)",
            (i+1, i+1, materials_for_phisics[i-16])
        )
        i += 1

    for lecture in lectures_for_informatics:
        cur.execute(
            "INSERT INTO lectures (lecture_id, lecture_name, course_id) VALUES (%s, %s, %s)",
            (i+1, lecture, 4)
        )
        cur.execute(
            "INSERT INTO lectures_materials (material_id , lecture_id, content) VALUES (%s, %s, %s)",
            (i+1, i+1, materials_for_informatics[i-24])
        )
        i += 1

    conn.commit()








def generate_groups():
    groups1 = [ 'ИС-1', 'ИС-2', 'ИС-3', 'ИС-4', 'ИС-5']
    groups2 = [ 'ИС-6', 'ИС-7', 'ИС-8', 'ИС-9', 'ИС-10']


    for group in groups1:
        cur.execute(
            "INSERT INTO groups (group_id, spec_id) VALUES (%s, %s)",
            (group, 1)
        )

    for group in groups2:
        cur.execute(
            "INSERT INTO groups (group_id, spec_id) VALUES (%s, %s)",
            (group, 2)
        )



def generate_students():
    from faker import Faker
    groups = [ 'ИС-1', 'ИС-2', 'ИС-3', 'ИС-4', 'ИС-5', 'ИС-6', 'ИС-7', 'ИС-8', 'ИС-9', 'ИС-10']
    fake = Faker('ru_RU')

    students = []


    student_id = 101
    for group in groups:
        for i in range(20):
            students.append(fake.name())
            cur.execute(
                "INSERT INTO students (student_id, name, group_id) VALUES (%s, %s, %s)",
                (student_id, students[i], group)

            )
            student_id += 1

def generate_schedule():

    groups1 = [ 'ИС-1', 'ИС-2', 'ИС-3', 'ИС-4', 'ИС-5'] # 2 subjects, 8 lectures in each
    groups2 = [ 'ИС-6', 'ИС-7', 'ИС-8', 'ИС-9', 'ИС-10'] # 2 subjects, 8 lectures in each




    for group in groups1:
        date1 = datetime(2023, 9, 2)
        date2 = datetime(2023, 9, 3)
        for i in range(1, 9):
            cur.execute(f"INSERT INTO schedule (group_id, lecture_id, date) VALUES ('{group}', {i}, '{date1}')")

            date1 += timedelta(days=14)
        for i in range(9, 17):
            cur.execute(f"INSERT INTO schedule (group_id, lecture_id, date) VALUES ('{group}', {i}, '{date2}')")

            date2 += timedelta(days=14)

    for group in groups2:
        date1 = datetime(2023, 9, 2)
        date2 = datetime(2023, 9, 3)

        for i in range(17, 25):

            cur.execute(f"INSERT INTO schedule (group_id, lecture_id, date) VALUES ('{group}', {i}, '{date1}')")
            date1 += timedelta(days=14)


        for i in range(25, 33):

                cur.execute(f"INSERT INTO schedule (group_id, lecture_id, date) VALUES ('{group}', {i}, '{date2}')")
                date2 += timedelta(days=14)
    conn.commit()

def generate_attendances():
    groups = ['ИС-1', 'ИС-2', 'ИС-3', 'ИС-4', 'ИС-5', 'ИС-6', 'ИС-7', 'ИС-8', 'ИС-9', 'ИС-10']



    st_k = 101
    for i in range(len(groups)):
        cur.execute(f"SELECT * FROM schedule WHERE group_id = '{groups[i]}'")
        lectures_of_group = cur.fetchall()
        for lecture in lectures_of_group:
            
            for j in range(20):
                student = st_k + j

                cur.execute(f"INSERT INTO attendances (student_id, lecture_id, date, attendance_status) VALUES ({student}, {lecture[1]}, '{lecture[2]}', {random.choice([True, False])})")
        st_k += 20

    conn.commit()



def clear_tables():
    cur.execute("DELETE FROM attendances")
    cur.execute("DELETE FROM schedule")
    cur.execute("DELETE FROM students")
    cur.execute("DELETE FROM groups")
    cur.execute("DELETE FROM lectures_materials")
    cur.execute("DELETE FROM lectures")
    cur.execute("DELETE FROM courses_in_spec")

    cur.execute("DELETE FROM courses")
    cur.execute("DELETE FROM Univ_spec")
    cur.execute("DELETE FROM spec")
    cur.execute("DELETE FROM cafedra")


    cur.execute("DELETE FROM univ")
    cur.execute("DELETE FROM univmain")
    conn.commit()

def generate_all_data():
    #clear_tables()
    generate_UniMain()
    conn.commit()
    time.sleep(10)

    generate_faculties()
    conn.commit()
    time.sleep(3)
    generate_cafedras()
    conn.commit()
    time.sleep(3)
    generate_specialities()
    conn.commit()
    time.sleep(3)
    generate_specialities_univ()
    conn.commit()
    time.sleep(3)

    generate_courses()
    conn.commit()
    time.sleep(3)
    generate_lecturers()
    conn.commit()
    time.sleep(3)
    generate_groups()
    conn.commit()
    time.sleep(3)
    generate_students()
    conn.commit()
    time.sleep(3)
    generate_schedule()
    conn.commit()
    time.sleep(3)
    generate_attendances()
    conn.commit()
    time.sleep(3)

    conn.commit()




    print('done')


