from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# Список товаров
products = [
    {"name": "Зеленый чай", "description": "Органический, богат антиоксидантами, 100 г", "price": 120, "rating": 4.8,
     "in_stock": 30},
    {"name": "Кофе арабика", "description": "Высшего сорта, средняя обжарка, 250 г", "price": 200, "rating": 4.7,
     "in_stock": 20},
    {"name": "Энергетический батончик", "description": "С кешью и клюквой, без сахара, 50 г", "price": 40,
     "rating": 4.9, "in_stock": 50},
    {"name": "Протеиновый коктейль", "description": "Шоколадный вкус, без лактозы, 500 мл", "price": 150, "rating": 4.6,
     "in_stock": 25},
    {"name": "Гречневая крупа", "description": "Цельнозерновая, предварительно промытая, 1 кг", "price": 90,
     "rating": 4.8, "in_stock": 40},
    {"name": "Оливки", "description": "Без косточек, в рассоле, 300 г", "price": 110, "rating": 4.7, "in_stock": 35},
    {"name": "Тофу", "description": "Нежный, для веганских блюд, 200 г", "price": 80, "rating": 4.5, "in_stock": 20},
    {"name": "Квиноа", "description": "Мультицветная, источник белка, 500 г", "price": 200, "rating": 4.9,
     "in_stock": 30},
    {"name": "Хумус", "description": "Классический, без добавок, 250 г", "price": 70, "rating": 4.8, "in_stock": 40},
    {"name": "Горький шоколад", "description": "Содержит 85% какао, поддерживает сердце, 100 г", "price": 95,
     "rating": 4.8, "in_stock": 45},
]


@app.route('/')
def home():
    return "Добро пожаловать на наш сервер продуктов!"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/products', methods=['GET'])
def get_products():
    app.logger.debug("Получен запрос к /products")
    query_name = request.args.get('name')
    query_description = request.args.get('description')
    query_min_price = request.args.get('min_price', type=int)
    query_max_price = request.args.get('max_price', type=int)

    filtered_products = products

    # Фильтрация товаров с использованием комплексных условий
    filtered_products = [
        product for product in filtered_products
        if (query_name.lower() in product["name"].lower() if query_name else True) and
           (query_description.lower() in product["description"].lower() if query_description else True) and
           (product["price"] >= query_min_price if query_min_price is not None else True) and
           (product["price"] <= query_max_price if query_max_price is not None else True)
    ]

    return jsonify(filtered_products)


if __name__ == '__main__':
    app.run(debug=False)
