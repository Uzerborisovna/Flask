from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Это наша временная "база данных" (просто список)
ads = []


# --- 1. GET: Получить все объявления ---
@app.route('/ads/', methods=['GET'])
def get_ads():
    return jsonify(ads), 200


# --- 2. POST: Создать новое объявление ---
@app.route('/ads/', methods=['POST'])
def create_ad():
    data = request.json

    # Проверяем, что пользователь прислал все нужные поля
    if not data or 'title' not in data or 'description' not in data or 'owner' not in data:
        return jsonify({"error": "Нужны поля: title, description, owner"}), 400

    # Создаем словарь (объявление)
    new_ad = {
        "id": len(ads) + 1,
        "title": data['title'],
        "description": data['description'],
        "created_at": datetime.now().isoformat(),  # Текущая дата
        "owner": data['owner']
    }

    # Сохраняем в наш список
    ads.append(new_ad)

    # Возвращаем созданное объявление и статус 201 (Created)
    return jsonify(new_ad), 201


# --- 3. DELETE: Удалить объявление по ID ---
@app.route('/ads/<int:ad_id>/', methods=['DELETE'])
def delete_ad(ad_id):
    global ads
    # Ищем объявление с нужным id
    for ad in ads:
        if ad['id'] == ad_id:
            ads.remove(ad)  # Удаляем из списка
            return jsonify({"message": f"Объявление {ad_id} удалено"}), 200

    return jsonify({"error": "Объявление не найдено"}), 404


# --- 4. PUT/PATCH: Редактировать объявление ---
# Используем PATCH, так как он позволяет менять только часть полей (например, только заголовок)
@app.route('/ads/<int:ad_id>/', methods=['PATCH'])
def update_ad(ad_id):
    data = request.json

    for ad in ads:
        if ad['id'] == ad_id:
            # Если пришло новое поле - обновляем, если нет - оставляем старое
            if 'title' in data:
                ad['title'] = data['title']
            if 'description' in data:
                ad['description'] = data['description']
            if 'owner' in data:
                ad['owner'] = data['owner']

            return jsonify(ad), 200

    return jsonify({"error": "Объявление не найдено"}), 404

if __name__ == '__main__':
    app.run(debug=True)