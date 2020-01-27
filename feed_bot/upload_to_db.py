import pymysql
import os


DB_HOST='localhost'
DB_USER=''
DB_PASSWORD=''
DB_NAME=''



def get_phrase():
	import_list = []
	file_dir = './text_clean'
	file_list = os.listdir(file_dir)
	for file in file_list:
		filepath = os.path.join(file_dir, file)
		import_list.append(filepath)

	return import_list



connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


import_list = get_phrase()
total = len(import_list)
count = 0
with connection.cursor() as cursor:
	for file in import_list:
		try:
			with open(file,'r') as f:
				body = f.read().strip()
			sql = "INSERT INTO `phrases` (`body`) VALUES (%s)"
			cursor.execute(sql, body)
			count += 1
			print('[{}/{}] Imported'.format(count, total))
		except:
			pass
connection.commit()