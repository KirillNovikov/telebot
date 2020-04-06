import sqlite3


def ensure_connection(func):
	def inner(*args,**kwargs):
		with sqlite3.connect('dbase.db') as connection:
			res = func(*args,connection=connection,**kwargs)
		return res
	return inner


@ensure_connection
def initialize_db(connection):
	cursor = connection.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS answers(
		variant TEXT NOT NULL,
		answer TEXT NOT NULL
		)
	""")
	connection.commit()


@ensure_connection
def get_answers_from_db(variant,connection):
	cursor = connection.cursor()
	cursor.execute("""
		SELECT * FROM answers WHERE variant=?
		
	""", (variant,))
	res = cursor.fetchone()
	connection.commit()
	return res[1]


@ensure_connection
def insert_answers_to_db(list_of_var_and_ans,connection): #см конец файла
	cursor = connection.cursor()
	for var_and_ans in list_of_var_and_ans:
		offset = var_and_ans.index('\n')
		ans = var_and_ans[offset+1:]
		var = var_and_ans[:offset]
		cursor.execute("""
			INSERT INTO answers (variant, answer) VALUES (?, ?)
			
		""", (var, ans))
	connection.commit()


# Ответы должны быть строго в том формате, который продемонстрирован в new_ans.txt, пробелы после ответов не допускаются
def get_ans(filename='new_ans.txt'):
	new_ans = open(filename).read()
	print(new_ans)
	return new_ans.split(sep='\n\n')


if __name__ == '__main__':
	'''
	a = get_ans()
	initialize_db()
	insert_answers_to_db(a)
	print('ok!')
	'''

	#Вставка ответа из кода, строго соблюдаем формат
	ans = """test
1 Закрытое общество
2 Фактор производства
3 56
4 135
5 31142
6 256
7 34
8 11221
9 135
10 15
11 234
12 124
13 14
14 11212
15 135
16 235
17 256
18 13323
19 13
20 317295
"""
	initialize_db()
	#insert_answers_to_db([ans]) #Принимает список
	print('ok!')

