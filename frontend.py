from boardgames import viable_game_list, load_data
from flask import Flask, request, render_template, send_from_directory, url_for
import os
app = Flask(__name__)


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

        result = viable_game_list(GAMES, players, owner, as_dataframe=True)
        
        #just_names = [game['Name'] for game in viable_game_list(GAMES, players, owner)]
        #return render_template('list.html', your_list=just_names)
        
        return render_template('tables.html', tables=[result.to_html(classes='games')], titles=['na', 'Available Games'])

    return '''<form method="post">
<input type="radio" name="owner" value="tricia">Tricia/Travis
<input type="radio" name="owner" value="ryan">Ryan/Sam
<input type="radio" name="owner" value="andrew">Sam/Andrew
<input type="radio" name="owner" value="alex">Alex
<input type="radio" name="owner" value="tim">Tim
<input type="radio" name="owner" value="evan">Evan
<p>Number of players:</p>
<input type="number" name="players" min="1" max="12" value="4">
<input type="submit">
</form>'''


if __name__ == '__main__':
	app.run(use_reloader=True)