from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

# Get User Information
# ---- Example -----
# username = "jdoe"
# password = "password1234"
# courses = ["CSE 123", "CSE 123", "COGS 456"]
# section_ids = ["066145", "066146", "066014"]
# WARNING: courses & section_ids MUST have equal amounts of elements in them.
username = ""
password = ""
courses = [""]
section_ids = [""]

# initialize the Chrome driver - to prevent the error https://github.com/SeleniumHQ/selenium/issues/10225
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# initialize the Chrome driver - normally
#driver = webdriver.Chrome("chromedriver")

# Go to WebReg
driver.get("https://act.ucsd.edu/webreg2")

# Find username input field and enter username
driver.find_element(By.ID, "ssousername").send_keys(username)

# Find password input field and enter username
driver.find_element(By.ID, "ssopassword").send_keys(password)

# Find and click login button
driver.find_element(By.CLASS_NAME, "sso-button").click()

# At this point I need to automate clicking the SSO button on my phone to automate 2FA verification
# I did so using an auto-clicker app in a single target location indefinity

# wait until the "Go" button appears and click it
WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, "startpage-button-go"))).click()


iterations = 0
# HEADS UP: If you want to run 3 iterations, leave it alone, otherwise change the 3 to a higher number.
while iterations < 3:
	# for every waitlisted course/section ID pair I'm trying to enroll into
	for i in range(len(courses)):
		# set variables for course and section ID pair
		course = courses[i]
		section_id = section_ids[i]

		# wait until you can enter course name
		search_bar = WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, "s2id_autogen1")))

		# clear the search_Bar and enter course name
		search_bar.clear()
		search_bar.send_keys(course)

		# select course in dropdown results
		drop_down = WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, "select2-result-label")))
		drop_down.click()

		# click dropdown triangle to view course details
		course_details = WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-icon-circlesmall-plus")))
		course_details.click()

		# locate desired section to enroll into
		target_section = WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '" + section_id + "')]")))

		# located desired section's enroll button
		enroll_button = target_section.find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "search-enroll-class")

		# if the enroll button is NOT enabled, let us know
		if not enroll_button.is_enabled():
			print("UNSUCCESSFUL (" + str(iterations) + ") : Cannot enroll into waitlisted course " + course + ", Section " + section_id)
		else:
			# If the enroll button is ENABLED, click that at the speed of light.
			enroll_button.click()

			# set variables for successful or not
			enroll_state = WebDriverWait(driver=driver, timeout=5).until(EC.presence_of_element_located((By.ID, "dialog-enroll")))
			error_state = WebDriverWait(driver=driver, timeout=5).until(EC.presence_of_element_located((By.CLASS_NAME, "error")))

			# Check if enrollment was successful or not
			if enroll_state is not None:

				# click "confirm"
				confirm_class = enroll_state.find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "ui-dialog-buttonset")
				confirm_button = WebDriverWait(driver=confirm_class, timeout=10).until(EC.visibility_of_all_elements_located((By.XPATH, ".//*")))
				confirm_button[2].click()

				# click "close" for enrollment success
				close_button0 = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.ID, "dialog-after-action-close")))
				close_button0.click()

				print("SUCCESSFUL (" + str(iterations) + ") : I MADE IT INTO WAITLISTED COURSE " + course + ", SECTION " + section_id)
			elif error_state is not None:
				print("(" + str(iterations) + ") Failure to enroll into waitlisted course " + course + ", Section " + section_id)

				# click "close" for enrollment failure
				close_button1 = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.ID, "dialog-after-action-close")))
				close_button1.click()
	# every while loop iteration, refresh the existing page to avoid having to do 2FA too much because it can bug out requests sent.
	driver.refresh()
	iterations += 1
	time.sleep(3) # added in 3 second buffer to not be too spammy. Can remove this line if you want no delay in the spam.

# Once we're done, close window and ChromeDriver instance
driver.quit()
print("Ran through all iterations set.")