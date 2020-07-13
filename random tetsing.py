import datetime
import psycopg2

#dat = datetime.date.today().strftime("%B_%d_%Y")

#print(dat)

connect = psycopg2.connect('dbname = jobs user=postgres password = amqm2001')
cursor = connect.cursor()