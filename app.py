from flask import Flask, render_template, request
import json

app = Flask(__name__)

def filter_data_by_budget(data, budget):
    filtered_data = {company: [car for car in cars if parse_price(car['fiyat']) <= float(budget)] for company, cars in data.items()}
    
    # Uygun araç varsa, ilk uygun aracı seç
    filtered_car = next((car for company, cars in filtered_data.items() for car in cars), None)
    
    return filtered_data, filtered_car



def parse_price(price):
    # Fiyatı uygun bir formata çevir ve float'a dönüştür
    price = price.split(" - ")[-1].replace(' TL', '').replace('.', '').replace(',', '')
    return float(price) if price.replace('.', '').isnumeric() else float('inf')

@app.route('/')
def index():
    # JSON dosyasından verileri yükle
    input_file_path = r"C:\Users\ozgur\OneDrive\Masaüstü\diğer_siteler.json"
    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Kullanıcının girdiği bütçe değerini al
    budget = request.args.get('budget')

    # Bütçe değeri var mı kontrol et
    if budget:
        try:
            # Bütçe bir float'a dönüştürülebiliyorsa, filtreleme işlemini gerçekleştir
            budget = float(budget)
            filtered_data = {company: [] for company in data.keys()}  # Filtrelenmiş veri için boş bir şablon oluştur
            for company, cars in data.items():
                for car in cars:
                    car_price = parse_price(car['fiyat'])
                    if car_price <= budget:
                        filtered_data[company].append(car)
        except ValueError:
            # Hatalı bir bütçe değeri girildiyse, tüm veriyi kullan
            filtered_data = data
    else:
        # Bütçe belirtilmemişse, tüm veriyi kullan
        filtered_data = data

    # Verilerle şablonu render et
    return render_template('index.html', data=filtered_data, budget=budget)

if __name__ == '__main__':
    app.run(debug=True)
