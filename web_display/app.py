from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime("%d %B %Y")
    return render_template('index.html', current_time=current_time , current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True)
    
