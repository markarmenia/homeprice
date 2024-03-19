from flask import Flask, render_template, request, redirect
import statistics
import psycopg2

app = Flask(__name__)

db_connection = psycopg2.connect(
    host="localhost",
    database="nshanyeghyan",
    user="nshanyeghyan",
    port="5432")


def select_car(car_make_input, car_model_input, year_from, year_to):
    cursor = db_connection.cursor()
    cursor.execute("SELECT price FROM car_database WHERE car_make = %s AND car_model = %s AND year BETWEEN %s AND %s", (car_make_input, car_model_input, year_from, year_to))
    rows = cursor.fetchall()
    if rows:
        prices = [row[0] for row in rows]
        average_price_round = round(statistics.median(prices))
        average_price = f'Շուկայական միջին գինը: ${average_price_round}'
        total_cars = f'Շուկայում վաճառքի առկա մոտավոր քանակ: {len(prices)}'
        car_details = f'{year_from}-{year_to} {car_make_input} {car_model_input}'
        return average_price, total_cars, car_details
    else:
        return f'Տեղեկություն չի գտնվել՝ փորձեք ընդլայնել տարեթվերը', f'Շուկայում վաճառքի առկա քանակ: 0', f'{year_from}-{year_to} {car_make_input} {car_model_input}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        car_make_input = request.form['car_make']
        car_model_input = request.form['car_model']
        year_from = request.form['year_from']
        year_to = request.form['year_to']

        average_price, total_cars, car_details = select_car(car_make_input, car_model_input, year_from, year_to)

        return render_template('main.html', average_price=average_price, total_cars=total_cars, car_details=car_details)

    return render_template('main.html')

@app.route('/aboutus')
def getaboutus():
    return render_template('aboutus.html')

@app.route('/aboutus', methods=['POST'])
def aboutus():
    return redirect('/aboutus')

@app.route('/contact')
def getcontact():
    return render_template('contact.html')

@app.route('/contact', methods=['POST'])
def contact():
    return redirect('/contact')

@app.route('/help')
def gethelp():
    return render_template('help.html')

@app.route('/help', methods=['POST'])
def help():
    return redirect('/help')

@app.route('/privacy')
def getprivacy():
    return render_template('privacy.html')

@app.route('/privacy', methods=['POST'])
def privacy():
    return redirect('/privacy')

if __name__ == '__main__':
    app.run(debug=True)        


from flask import Flask, render_template, request, redirect
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# import time
# import psycopg2
# import statistics
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# app = Flask(__name__)

# db_connection = psycopg2.connect(
#     host="localhost",
#     database="nshanyeghyan",
#     user="nshanyeghyan",
#     port="5432")


# chrome_driver_path = '/Users/nshanyeghyan/Desktop/python/chromedriver-mac-arm64/chromedriver'

# def select_car(car_make_input, car_model_input, year_from, year_to):
#     cursor = db_connection.cursor()
#     cursor.execute("SELECT average_price, total_cars FROM car_prices WHERE car_make = %s AND car_model = %s AND year_from = %s AND year_to = %s", (car_make_input, car_model_input, year_from, year_to))
#     row = cursor.fetchone()
#     if row:
#         average_price, total_cars = row
#         return [], f'Շուկայական միջին գինը: ${average_price}', f'Շուկայում վաճառքի առկա քանակ: {total_cars}'

#     service = Service(executable_path=chrome_driver_path)
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(service=service, options=options)

#     try:
#         driver.get("https://www.list.am/category/23")

#         drop = driver.find_element(By.XPATH, '//*[@id="ff"]/div[3]/div/div[2]')
#         drop.click()
#         time.sleep(2)
#         car_make = driver.find_element(By.CSS_SELECTOR, f'div[data-name="{car_make_input}"]')
#         car_make.click()
#         time.sleep(2)
#         drop2 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//*[@id="ff"]/div[3]/div[2]/div[2]/div'))
#         )
#         drop2.click()
#         time.sleep(2)

#         try:
#             car_model = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, f'//div[@data-name="{car_model_input}" and @class="i"]'))
#         )
#             car_model.click()
#             time.sleep(2)
#         except TimeoutException:
#             average_price = 0
#             total_cars = 0
#             return [], f'Ընտրեք ճիշտ մոդել', f'Շուկայում վաճառքի առկա քանակ: {total_cars}'

#         drop3 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//*[@id="ff"]/div[7]/div[2]/div[2]/div[1]'))
#         )
#         drop3.click()
#         time.sleep(2)
#         year_1 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, f'//div[@data-name="{year_from}" and @class="i"]'))
#         )
#         year_1.click()
#         time.sleep(2)

#         drop4 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//*[@id="ff"]/div[7]/div[2]/div[2]/div[2]'))
#         )
#         drop4.click()
#         time.sleep(2)

#         year_2 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, f'//div[@class="l top" and @data-searchname="Որոնում"]/div[@data-value="{year_to}"]'))
#         )
#         year_2.click()
#         time.sleep(2)

#         try:
#             no_results_element = driver.find_element(By.XPATH, '//*[@id="contentr"]/div[1]/div')
#             if 'Ձեր հարցմանը համապատասխան տեղեկություն չի գտնվել:' in no_results_element.text:
#                 average_price = 0
#                 total_cars = 0
#                 return [], f'Տեղեկություն չի գտնվել', f'Շուկայում վաճառքի առկա քանակ: {total_cars}'
#         except NoSuchElementException:
#             pass

#         prices = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CLASS_NAME, 'p'))
#         )

#         drop5 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//*[@id="ff"]/div[9]/div[5]/div[2]/div'))
#         )
#         drop5.click()
#         time.sleep(2)

#         custom = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//div[@class="l top" and @data-searchname="Որոնում"]/div[@data-value="1"]'))
#         )
#         custom.click()
#         time.sleep(2)

#         res_json = []

#         while True:
#             try:
#                 # Scraping prices on the current page
#                 prices = WebDriverWait(driver, 10).until(
#                     EC.presence_of_all_elements_located((By.CLASS_NAME, 'p'))
#                 )

#                 for price in prices:
#                     car_price = price.text.strip()
#                     if '֏' in car_price:
#                         numeric_price = ''.join(char for char in car_price if char.isdigit())
#                         numeric_price = int(numeric_price)
#                         numeric_price = numeric_price / 404.35
#                         res_json.append(numeric_price)
#                     elif '€' in car_price:
#                         numeric_price = ''.join(char for char in car_price if char.isdigit())
#                         numeric_price = int(numeric_price)
#                         numeric_price = (numeric_price * 437.67)/404.35
#                         res_json.append(numeric_price)
#                     elif '₽' in car_price:
#                         numeric_price = ''.join(char for char in car_price if char.isdigit())
#                         numeric_price = int(numeric_price)
#                         numeric_price = (numeric_price * 4.35)/404.35
#                         res_json.append(numeric_price)
#                     else:
#                         numeric_price = ''.join(char for char in car_price if char.isdigit())
#                         numeric_price = int(numeric_price)
#                         res_json.append(numeric_price)

#                 # Click on the "Հաջորդը >" link if available
#                 try:
#                     next_page_link = WebDriverWait(driver, 5).until(
#                         EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Հաջորդը >")]'))
#                     )
#                     next_page_link.click()
#                     time.sleep(2)
#                 except:
#                     # Break the loop if the link is not present
#                     break
#             except TimeoutException:
#                 average_price = 0
#                 total_cars = 0
#                 return [], f'Տեղեկություն չի գտնվել', f'Շուկայում վաճառքի առկա քանակ: {total_cars}'
#     finally:
#         driver.quit()
#     av_price = round(statistics.median(sorted(res_json))) #round(sum(res_json) / len(res_json))
#     average_price = f'Շուկայական միջին գինը: ${av_price}' if res_json else 'Արդյունքներ չկան'
#     total_cars = f'Շուկայում վաճառքի առկա քանակ: {len(res_json)}'
#     cursor = db_connection.cursor()
#     cursor.execute("INSERT INTO car_prices (year_from, year_to, car_make, car_model, average_price, total_cars) VALUES (%s, %s, %s, %s, %s, %s)", 
#                     (year_from, year_to, car_make_input, car_model_input, av_price, len(res_json)))
#     db_connection.commit()
#     cursor.close()
#     return res_json, average_price, total_cars

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         car_make_input = request.form['car_make']
#         car_model_input = request.form['car_model']
#         year_from = request.form['year_from']
#         year_to = request.form['year_to']

#         res_json, average_price, total_cars = select_car(car_make_input, car_model_input, year_from, year_to)

#         return render_template('main.html', res_json=res_json, average_price=average_price, total_cars=total_cars)

#     return render_template('main.html')

# @app.route('/aboutus')
# def getaboutus():
#     return render_template('aboutus.html')

# @app.route('/aboutus', methods=['POST'])
# def aboutus():
#     return redirect('/aboutus')

# @app.route('/contact')
# def getcontact():
#     return render_template('contact.html')

# @app.route('/contact', methods=['POST'])
# def contact():
#     return redirect('/contact')

# @app.route('/help')
# def gethelp():
#     return render_template('help.html')

# @app.route('/help', methods=['POST'])
# def help():
#     return redirect('/help')

# @app.route('/privacy')
# def getprivacy():
#     return render_template('privacy.html')

# @app.route('/privacy', methods=['POST'])
# def privacy():
#     return redirect('/privacy')

# if __name__ == '__main__':
#     app.run(debug=True)        

# # car_make_input = input("Enter the car make: ")
# # car_model_input = input("Enter the car model: ")
# # year_from = input("Enter the year from: ")



# # select_car(car_make_input, car_model_input, year_from)



#     # driver.find_element(By.ID, "first-name").send_keys("John")
#     # driver.find_element(By.ID, "last-name").send_keys("Doe")
#     # driver.find_element(By.ID, "job-title").send_keys("PM")
#     # driver.find_element(By.ID, "radio-button-2").click()
#     # driver.find_element(By.ID, "checkbox-1").click()
#     # driver.find_element(By.CSS_SELECTOR, 'option[value="1"]').click()
#     # driver.find_element(By.ID, 'datepicker').send_keys("01/01/2022")
#     # driver.find_element(By.ID, 'datepicker').send_keys(Keys.RETURN)
#     # driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-primary").click()
#     # WebDriverWait(driver, 10).until(
#     #         EC.presence_of_all_elements_located((By.CLASS_NAME, 'alert'))
#     #     )
#     # time.sleep(2)


#     #radio2 = driver.find_element(By.CSS_SELECTOR, 'input[value="checkbox-2"]')
#     #radio3 = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/input')
#     #radio3.click()
#     #actions = ActionChains(driver)
#     #actions.click_and_hold(image).move_to_element(box).release().perform()
#     #driver.execute_script("arguments[0].click();", closebutton)
#     #actions = ActionChains(driver)s
#     #actions.move_to_element(name).perform() scroll to element
#     #name.send_keys("Mark Yeg") add text
#     # date.send_keys(Keys.RETURN) press Enter
#     #original_tab = driver.window_handles[0]
#     #alert = driver.switch_to.alert()
# #dropdown.select_by_visible_text("Option 1")
# #dropdown.select_by_index(1)  # Selects the second option
# #dropdown.select_by_value("option3")


