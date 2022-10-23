import sqlite3
import re

#Добавляем задание в бд
def add_task(idUser,task, name_of_sub, username):
    connect = sqlite3.connect('homework.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO homework (`userId`, `task`,`subject`,`username`) VALUES (?,?,?,?)',(idUser,task, name_of_sub, username))
    connect.commit()
    cursor.close()

#Ввывод данных
def show_task(name_of_sub):
    connect = sqlite3.connect('homework.db')
    cursor = connect.cursor()
    cursor.execute('SELECT `task`,`username`  FROM homework WHERE `subject` like ?',(name_of_sub,))
    data = cursor.fetchall()
    tasks = []

    for i in data:
        tasks.append(i)

    task_re = []
    for i in range(len(data)):
        regex = re.sub('|\(|\'|\,|\)','', str(tasks[i]))
        task_re.append(regex)

    final =[]

    for i in task_re:
        final_result = i + '\n'
        final.append(final_result)

    final_data = '\n'.join(final)
    if len(final_data) == 0:
        list_is_empty = "Завдань по данному предмету ще немає)"
        return list_is_empty
    else:
        return final_data

# def get_id_by_task(task):
#     connect = sqlite3.connect('homework.db')
#     cursor = connect.cursor()
#     cursor.execute('SELECT FROM `userId` FROM where `task` = ?',(task,))

#Test delete
def delete_task(task, subject, user_id):
    connect = sqlite3.connect('homework.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM homework where `task`=? and `subject` =? and `userId` =?', (task, subject, user_id))
    connect.commit()
    cursor.close()

