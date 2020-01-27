import pymysql
import praw

from random import randint
from datetime import datetime

REDDIT_CLIENT_ID=''
REDDIT_CLIENT_SECRET=''
REDDIT_USER_AGENT='my user agent'
REDDIT_USERNAME=''
REDDIT_PASSWORD=''

DB_HOST='localhost'
DB_USER=''
DB_PASSWORD=''
DB_NAME=''

TODAY = datetime.strftime(datetime.now(), '%Y-%m-%d')


def get_reddit():

	reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
					client_secret=REDDIT_CLIENT_SECRET,
					user_agent=REDDIT_USER_AGENT,
					username=REDDIT_USERNAME,
					password=REDDIT_PASSWORD)

	return reddit

def get_connection():

	connection = pymysql.connect(host=DB_HOST,
								user=DB_USER,
								password=DB_PASSWORD,
								db=DB_NAME,
								charset='utf8mb4',
								cursorclass=pymysql.cursors.DictCursor)
	return connection


def get_keywords(connection):
	keywords_list = []
	
	with connection.cursor() as cursor:
		sql = 'SELECT * FROM keywords'
		cursor.execute(sql)

	for result in cursor.fetchall():
		keywords_list.append(result)

	return keywords_list

def get_subreddits(connection):
	subreddits_list = []
	
	with connection.cursor() as cursor:
		sql = 'SELECT * FROM subreddits'
		cursor.execute(sql)

	for result in cursor.fetchall():
		subreddits_list.append(result)

	return subreddits_list

def check_already_commented(subreddit):
	sql = 'SELECT * FROM history WHERE subreddit_name = "{}" AND commented_date = "{}"'.format(subreddit.name, TODAY)

	with connection.cursor() as cursor:
		cursor.execute(sql)
		result = cursor.fetchone()
	if result:
		return True
	else:
		return False


def get_submissions_list(subreddit):
	
	submissions_list = []

	for submission in subreddit.hot(limit=10):
		submissions_list.append(submission)
	for submission in subreddit.new(limit=10):
		submissions_list.append(submission)

	return submissions_list

def parse_keywords(keywords_list, comment):
	for keyword in keywords_list:
		try:
			if keyword['keyword'] in comment.body.lower():
				return keyword
			else:
				pass
		except Exception as e:
			return False

	return False

def choose_answer(connection, keyword):
	answers_list = []

	with connection.cursor() as cursor:
		sql = 'SELECT * FROM phrases WHERE body LIKE "%{}%" AND used = 0'.format(keyword['keyword'])
		cursor.execute(sql)
		for result in cursor.fetchall():
			if len(result['body']) < 260:
				answers_list.append(result)

	count = 0
	total_answers = len(answers_list)
	parts_number = randint(1,3)
	beta = []

	while count <= parts_number:
		count += 1
		choice = randint(0, total_answers)
		part = answers_list[choice]
		beta.append(part['body'])

	answer = ' '.join(beta)

	return answer


def update_history(connection, subreddit, submission, keyword):
	with connection.cursor() as cursor:
		sql = 'INSERT INTO history (subreddit_name,submission_id, commented_date, keyword) VALUES ("{}","{}","{}","{}")'.format(subreddit.name, submission.name, TODAY, keyword['keyword'])
		cursor.execute(sql)
		connection.commit()

connection = get_connection()
reddit = get_reddit()
keywords_list = get_keywords(connection)
subreddits_list = get_subreddits(connection)


for entry in subreddits_list:
	subreddit = reddit.subreddit(entry['subreddit'])
	commented_today = check_already_commented(subreddit)
	
	if commented_today is False:
	
		submissions_list = get_submissions_list(subreddit)
		for submission in submissions_list:
			if commented_today is False:
				for comment in submission.comments.list():
					keyword = parse_keywords(keywords_list, comment)
					if keyword:
						
						answer = choose_answer(connection, keyword)
						print('\n\n')
						print('=== {} {} ==============================\n'.format(subreddit.display_name, subreddit.name))
						print(comment.body)
						print('-----------------\n')
						print(answer)
						print('-----------------\n')
						print('\n===============')
		
						comment.reply(answer)
						update_history(connection, subreddit, submission, keyword)
						commented_today = True
		
						break



