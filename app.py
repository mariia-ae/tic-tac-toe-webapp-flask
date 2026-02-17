from flask import Flask, render_template, request, jsonify
import game

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
     data = request.json
     result = game.make_move(
          data["row"],
          data["col"],
          data.get("mode", "pvp")
     )
     return jsonify(result)

@app.route("/reset", methods=["POST"])
def reset():
     game.reset_game()
     return jsonify({"status": "reset"})
if __name__=="__main__":
     app.run(debug=True)
