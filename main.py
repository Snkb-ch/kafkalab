import random
from datetime import datetime, timedelta

import elasticsearch
import redis
from transfer import *
# Подключение к Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


from generator import *
from pymongo import MongoClient

from prettytable import PrettyTable



mongo_client = MongoClient('mongodb://localhost:27017/')


db_mongo = mongo_client['my_database']


from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "99679926"
driver = GraphDatabase.driver(uri, auth=(username, password))


from elasticsearch import Elasticsearch


try:
    es = Elasticsearch(
        hosts=[
                "http://localhost:9200"
        ],
        http_auth=('elastic', 'bC6=esR3GJvEaS9U5KR*'),
        use_ssl=False,
        verify_certs=False,
        ca_certs=None,
    )



except:
   pass


import psycopg2


conn  = psycopg2.connect(
    user="root",
    password="9967992",
    host="localhost",
    port="5433",
    database="postgres"  # Или другое имя базы данных, если она была создана
)

cur = conn.cursor()





def get_student(student_id):
    student  = redis_client.get(student_id)

    # to json
    student = json.loads(student)
    return student['name']




def get_lectures_by_word(word):

    if word == '':
        word = 'основы'

    res = es.search(index="materials", body={"size": 10000,   "query": {"match": {"content": word}}})

    lectures = []
    for hit in res['hits']['hits']:
        lectures.append(hit['_source']['lecturer_id'])
    print('lectures: ', lectures)
    return list(set(lectures))


def get_procent_of_attendances(lectures, start_date, end_date, word):
    if start_date == '':
        start_date = '2023-09-01'
    if end_date == '':
        end_date = '2023-12-30'
    if word == '':
        word = 'основы'




    students = []
    group_lectures = {}




    for lecture in lectures:
        with driver.session() as session:
            query = f"""
            
MATCH (sp:Spec)-[:INCLUDES_COURSE]->(c:Course)-[:INCLUDES_LECTURE]->(l:Lecture) 
            WHERE l.id = {lecture}
MATCH (sp)-[:INCLUDES_GROUP]->(g:Group)
MATCH (st:Student)-[:MEMBER_OF]->(g:Group)
            RETURN st.id
            """
            students_in_group = session.run(query).values()



        students.extend(students_in_group)
    print(students_in_group)



    # sheldue count lectures for group in period of time and add in group_lectures

    for lecture in lectures:
        cur.execute(f"SELECT group_id, COUNT(*) FROM schedule WHERE date BETWEEN '{start_date}' AND '{end_date}' AND lecture_id = {lecture} GROUP BY group_id")
        result = cur.fetchall()
        for group in result:
            if group[0] in group_lectures:
                group_lectures[group[0]] += group[1]
            else:
                group_lectures[group[0]] = group[1]


    # students nly values in list not lists in list
    students = [item for sublist in students for item in sublist]


    count_lec = 0


    students = list(set(students))
    print(students)

    students_lec = {}
    for student in students:
        # get group for student and count of lectures for this group in period of time and add in students_lec
        with driver.session() as session:

            grou = session.run(f"MATCH (s:Student)-[:MEMBER_OF]->(g:Group) WHERE s.id = {student} RETURN g.id").values()

        try:
            group = grou[0][0]
        except:
            print(grou)
        if group in group_lectures:
            count_lec = group_lectures[group]
        else:
            count_lec = 0
        students_lec[student] = count_lec


    # cur.execute(
    #     f"SELECT student_id, ROUND(((COUNT(*) FILTER (WHERE attendance_status = true)::decimal / COUNT(*)::decimal) * 100),2)  AS attendance_percentage FROM attendances WHERE date BETWEEN '{start_date}' AND '{end_date}' AND lecture_id = ANY (%s) AND student_id = ANY (%s) GROUP BY student_id ORDER BY attendance_percentage ASC LIMIT 10",
    #     (lectures, students))

    cur.execute(
        f"SELECT student_id, COUNT(*) FILTER (WHERE attendance_status = true) FROM attendances WHERE date BETWEEN '{start_date}' AND '{end_date}' AND lecture_id = ANY (%s) AND student_id = ANY (%s) GROUP BY student_id",
        (lectures, students))

    result = cur.fetchall()


    students_attendances = {}
    for student in result:
        students_attendances[student[0]] = student[1]



    for student in students:

        if student in students_attendances:
            students_attendances[student] = round((students_attendances[student] / students_lec[student]) * 100, 2)
        else:
            students_attendances[student] = 0

    # sort students by procent of attendances
    result = sorted(students_attendances.items(), key=lambda x: x[1], reverse=False)




    table = PrettyTable()

    table.field_names = ["Student ID", "ФИО", "Посещаемость", "Слово", "Start Date", "End Date", 'Группа']

    for student in result[:10]:
        with driver.session() as session:

            group = session.run(
                f"MATCH (s:Student)-[:MEMBER_OF]->(g:Group) WHERE s.id = {student[0]} RETURN g.id").values()

        group = group[0][0]







        table.add_row([student[0], get_student(student[0]), student[1], word, start_date, end_date, group])

    print(table)



    













while True:
    print('\n')
    print("Нажмите 1 для очистки всех данных")
    print("Нажмите 2 для генерации всех данных")
    print("Нажмите 3 для получения всех данных из Redis")
    print("Нажмите 4 для получения всех данных из MongoDB")
    print("Нажмите 5 для переноса данных")
    print("Нажмите 6 для очистки postgres")
    print("Нажмите 7 для выполниния запроса")
    print("Нажмите 8 для получения всех данных из Elasticsearch")
    a = int(input())
    if a == 1:
        clear_tables()
        clear_all()

    elif a == 2:

        generate_all_data()
    elif a == 3:
        get_all_from_redis()

    elif a == 5:
        transfer_all()
    elif a == 6:
        clear_tables()

    elif a == 7:
        start_date = input('Введите начальную дату: ')
        end_date = input('Введите конечную дату: ')
        word = input('Введите слово: ')
        get_procent_of_attendances(get_lectures_by_word(word), start_date, end_date, word)

    elif a == 8:
        get_all_from_elasticsearch()
