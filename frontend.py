from boardgames import viable_game_list, load_data
from flask import Flask, request, render_template, send_from_directory, url_for
app = Flask(__name__)
app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))

GAMES = load_data()

#@app.route('/')
#def homepage():
#    return """<h1>Genny Games</h1>"""

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        owner = request.form.getlist('owner')[0]
        players = int(request.form.getlist('players')[0])
        just_names = [game['Name'] for game in viable_game_list(GAMES, players, owner)]
        return render_template('list.html', your_list=just_names)

    return '''<form method="post">
<input type="checkbox" name="owner" value="tricia">Tricia/Travis<br>
<input type="checkbox" name="owner" value="ryan">Ryan/Sam<br>
<input type="checkbox" name="owner" value="andrew">Sam/Andrew<br>
<input type="checkbox" name="owner" value="alex">Alex<br>
<input type="checkbox" name="owner" value="tim">Tim<br>
<input type="checkbox" name="owner" value="evan">Evan<br>
<input type="number" name="players" min="1" max="12" value="4">
<input type="submit">
</form>'''

#app.run()

if __name__ == '__main__':
    app.run(use_reloader=True)