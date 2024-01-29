import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import locale
from selenium.webdriver.chrome.options import Options


locale.setlocale(locale.LC_NUMERIC, "tr_TR.UTF-8")


def convert_to_turkish_number_format(price_text):
    try:
        # Fiyatı float'a çevirme
        price = float(price_text.replace('₺', '').replace('.', '').replace(',', '').strip())

        # Fiyatı formatlayarak geri döndürme (virgül ve ondalık kısmı kaldırma)
        formatted_price = '{:,.0f}'.format(price)[:-3].replace(',', '.')
        return formatted_price + ' TL'
    except ValueError:
        return price_text[:-6].strip()


def convert_to_turkish_number_format2(price_text):
    try:
        price = float(price_text.replace('₺', '').replace('.', '').replace(',', '').strip())

        # Sayıyı bir birim sola kaydırıp ilk 5 birimi alıyoruz.
        shifted_price = int(price * 10)
        formatted_price = '{:,.0f}'.format(shifted_price)[:5].replace(',', '.')

        # Sonrasına TL ekliyoruz.
        return f"{formatted_price} TL"
    except ValueError:
        return price_text




driver_avis = webdriver.Chrome()
driver_enterprise = webdriver.Chrome()
driver_budget = webdriver.Chrome()
driver_europcar = webdriver.Chrome()
driver_avec = webdriver.Chrome()

url1 = "https://www.avis.com.tr/rezervasyon/araciniz?id=IO_hMHEuGFriXGURTW8Qp45TMSALpHD0PWICaR4PpgtUy6XrrH3XY40p384fKQejXQwEw9W6IlKAI3L211yK7Sq_yIMPujH_EPyogDOqSKinBzNnp3DmGXVlSkE6X5end_l_pmH80N7x31mX_w4aAg&utm_referrer=https%3A%2F%2Fwww.avis.com.tr%2F"
driver_avis.get(url1)

url2 = "https://www.enterprise.com.tr/rezervasyon/istanbul-havalimani-arac-kiralama?dropOffLocation=istanbul-havalimani-arac-kiralama&start=2024-01-22T12:00&end=2024-01-24T12:00&age=21-24&campaign"
driver_enterprise.get(url2)

url3 = "https://www.budget.com.tr/rezervasyon/araciniz?id=plF8QHdeMryQM0tW_DAAMSrTQwEpC38b2BSZY3KJo2cSMSSw4MwS9v4T1E-e4Ydwt05Cb2vqFJXFzWFj7jzokG8pGNLnT0GKl_eXJre3vW4"
driver_budget.get(url3)

url4 = "https://www.europcar.com.tr/Reservations?StartDate=23.01.2024&EndDate=24.01.2024&StartTime=09%3A00&EndTime=04%3A00&StartOfficeCode=IST&EndOfficeCode=IST&Type=vehicle&EntityId=2cdfa3e3-654d-4a1a-9db9-2f75481d0164"
driver_europcar.get(url4)

url5 = "https://www.avecrentacar.com/tr/search-car?pickup_branch_id=49&dropoff_branch_id=49&pickup_date=2024-01-23T08:00:00&dropoff_date=2024-01-25T08:00:00"
driver_avec.get(url5)

wait_avis = WebDriverWait(driver_avis, 30)
wait_avis.until(EC.presence_of_element_located((By.CLASS_NAME, "car-model")))

wait_enterprise = WebDriverWait(driver_enterprise, 30)
wait_enterprise.until(EC.presence_of_element_located((By.CLASS_NAME, "car__list-item-inner")))

wait_budget = WebDriverWait(driver_budget, 30)
wait_budget.until(EC.presence_of_element_located((By.CLASS_NAME, "car-model")))

wait_europcar =WebDriverWait(driver_europcar, 30)
wait_europcar.until(EC.presence_of_element_located((By.CLASS_NAME, "col-10")))

wait_avec =WebDriverWait(driver_avec, 30)
wait_avec.until(EC.presence_of_element_located((By.CLASS_NAME, "car-title-area")))

avis_data = []
enterprise_data = []
budget_data = []
europcar_data = []
avec_data = []

# AVİS KISMI
car_container1 = driver_avis.find_element(By.CLASS_NAME, "primary-vehicle-card-list")
car_elements1 = car_container1.find_elements(By.XPATH, "//div[contains(@class, 'card-front')]")
for car_element in car_elements1:
    car_model_data1 = car_element.find_element(By.CLASS_NAME, "car-model").text
    price_element1 = car_element.find_element(By.XPATH, ".//span[@class='price']")
    price_text1 = convert_to_turkish_number_format(price_element1.text)
    if price_text1:
        avis_data.append({"model": car_model_data1, "fiyat": price_text1})

# ENTERPRISE KISMI
car_container2 = driver_enterprise.find_element(By.CLASS_NAME, "car__list")
car_elements2 = car_container2.find_elements(By.XPATH, "//div[contains(@class, 'car__list-item-inner')]")
for car_element in car_elements2:
    car_model_data2 = car_element.find_element(By.CLASS_NAME, "title").text
    price_element2 = car_element.find_element(By.XPATH, ".//div[@class='price']")
    price_text2 = convert_to_turkish_number_format2(price_element2.text)
    if price_text2:
        enterprise_data.append({"model": car_model_data2, "fiyat": price_text2})

# BUDGET KISMI
car_container3 = driver_budget.find_element(By.CLASS_NAME, "primary-vehicle-card-list")
car_elements3 = car_container3.find_elements(By.XPATH, "//div[contains(@class, 'card-front')]")
for car_element in car_elements3:
    car_model_data3 = car_element.find_element(By.CLASS_NAME, "car-model").text
    price_element3 = car_element.find_element(By.XPATH, ".//span[@class='price']")
    price_text3 = convert_to_turkish_number_format(price_element3.text)
    if price_text3:
        budget_data.append({"model": car_model_data3, "fiyat": price_text3})

# EUROPCAR KISMI
car_container4 = driver_europcar.find_element(By.XPATH, "//div[contains(@class, 'col-sm-12 col-12 mb-2 carlist res-carItem')] ")
car_elements4 = car_container4.find_elements(By.XPATH, "//div[contains(@class, 'row car onoffer sidePadding')]")
for car_element in car_elements4:
    car_model_data4 = car_element.find_element(By.XPATH, ".//h3").text
    price_element4 = car_element.find_element(By.CLASS_NAME, "prevpayValue")
    price_text4 = convert_to_turkish_number_format2(price_element4.text)
    if price_text4:
        europcar_data.append({"model": car_model_data4, "fiyat": price_text4})

# AVEC KISMI
car_container5 = driver_avec.find_element(By.XPATH, "//div[contains(@class, 'card mb-3')]")
car_elements5 = car_container5.find_elements(By.XPATH, ".//div[contains(@class, 'card-body row cars-detail')]")
for car_element in car_elements5:
    car_model_element5 = car_element.find_element(By.XPATH, ".//div[contains(@class, 'car-title-area')]")
    car_model_data5 = car_model_element5.text.strip()

    price_element5 = car_element.find_element(By.CLASS_NAME, "last-price")
    price_text5 = convert_to_turkish_number_format(price_element5.text)

    if car_model_data5 and price_text5:
        avec_data.append({"model": car_model_data5, "fiyat": price_text5})

# Selenium'u kapatma
driver_avis.quit()
driver_enterprise.quit()
driver_budget.quit()
driver_europcar.quit()
driver_avec.quit()

# JSON dosyasına yazma
output_data = {"avis": avis_data, "enterprise": enterprise_data,"budget": budget_data, "europcar": europcar_data, "avec": avec_data}
output_file_path = r"C:\Users\ozgur\OneDrive\Masaüstü\diğer_siteler.json"

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=2)

print(f"Veriler başarıyla '{output_file_path}' dosyasına kaydedildi.")




