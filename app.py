from flask import Flask, render_template, request, url_for
import requests

app = Flask(__name__)

API_KEY = "83ff146b76a94fa088f0ba8e8ca39617"
BASE_URL = "https://api.rawg.io/api/games"

contact_images = ["contact.png"]  # ใส่ชื่อไฟล์รูปใน static

@app.route("/", methods=["GET", "POST"])
def index():
    games = []
    query = ""
    selected_game = None
    show_contact = False

    # ตรวจสอบว่าเรียกหน้าติดต่อ
    if request.args.get("contact") == "1":
        show_contact = True
        return render_template("index.html", games=games, query=query,
                               selected_game=selected_game,
                               show_contact=show_contact,
                               contact_images=contact_images)

    # ตรวจสอบว่ากดดูรายละเอียดเกม
    game_id = request.args.get("game_id")
    if game_id:
        params = {"key": API_KEY}
        response = requests.get(f"{BASE_URL}/{game_id}", params=params)
        if response.status_code == 200:
            selected_game = response.json()

    # ค้นหาเกม
    if request.method == "POST":
        query = request.form.get("search")
        if query:
            params = {"key": API_KEY, "search": query}
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                games = data.get("results", [])
    else:
        # หน้าแรก: แสดงเกมฮิต
        params = {"key": API_KEY, "ordering": "-added", "page_size": 12}
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            games = data.get("results", [])

    return render_template("index.html", games=games, query=query,
                           selected_game=selected_game,
                           show_contact=show_contact,
                           contact_images=contact_images)

if __name__ == "__main__":
    app.run(debug=True)
