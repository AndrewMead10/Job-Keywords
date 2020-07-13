from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import psycopg2
import time
import datetime
import multiprocessing


#assert opts.headless

connect = psycopg2.connect('dbname = jobs user=postgres password = amqm2001')
cursor = connect.cursor()
connect.set_client_encoding('WIN1252')
connect.commit()
day = str(datetime.date.today().strftime("%B_%d_%Y"))

def serverConnect():
	table = 'create table ' + day + '(JobName text, JobCompany text, JobLocation text, JobSalary text, JobDesc text);'
	cursor.execute(table);
	connect.commit();

def run(url):

	opts = Options()
	opts.headless = True
	browser = Chrome(chrome_options = opts)
	browser.get('https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK')
	user_name = browser.find_element_by_id('userEmail')
	user_name.send_keys('thatgu98@gmail.com')
	pswrd = browser.find_element_by_id('userPassword')
	pswrd.send_keys('Zaq12wsx')
	pswrd.submit()
	time.sleep(5)
	actions = ActionChains(browser)
	browser.get(url)
	time.sleep(5)
	listings_all = browser.find_element_by_class_name('jlGrid')
	listings = listings_all.find_elements_by_tag_name('li')
	for i in range(30):
		actions.move_to_element(listings[i]).click().perform()

		try:
			desc = browser.find_element_by_class_name('jobDescriptionContent')
			desc = desc.text
		except:
			desc = 'desc not available'
			print(desc)
		try:
			job = browser.find_element_by_class_name('title')
			job = job.text
		except:
			job = 'job name not available'
			print(job)
		try:
			location = browser.find_element_by_class_name('location')
			location = location.text
		except:
			location = 'location not available'
			print(location)
		try:
			salary = browser.find_element_by_class_name('salary')
			salary = salary.text
		except:
			salary = 'salary not available'
			print(salary)
		try:
			company = browser.find_element_by_class_name('employerName')
			company = company.text
		except:
			company = 'company not available'
			print(company)


		cursor.execute('insert into '  + day + ' values (%s, %s, %s, %s, %s)', (job, company, location, salary, desc));
		connect.commit();






if __name__ == '__main__':

	serverConnect()
	jobs = []
	for i in range(1,6):
		p = multiprocessing.Process(target = run, args = (('https://www.glassdoor.com/Job/us-computer-science-jobs-SRCH_IL.0,2_IN1_KO3,19_IP' + str(i) +'.htm'),))
		jobs.append(p)
		p.start()





		





