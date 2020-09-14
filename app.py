from flask import Flask, render_template, request, redirect
import numpy as numpy
import joblib
import sklearn

app = Flask(__name__)

#Loading the model
model = joblib.load('models/random_forest.pkl')

#Home page template 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        try:

            #Get values from html page
            batting_team = request.form['batting']
            bowling_team = request.form['bowling']
            score_10 = int(request.form['score'])
            wicket_10 = int(request.form['wicket'])

            #Convert choices to one hot
            def teams_to_onehot(choice):
                switcher = {
                    'csk': [0, 0, 0, 0, 0, 0, 0],
                    'dc': [1, 0, 0, 0, 0, 0, 0],
                    'kxip': [0, 1, 0, 0, 0, 0, 0],
                    'kkr': [0, 0, 1, 0, 0, 0, 0],
                    'mi': [0, 0, 0, 1, 0, 0, 0],
                    'rr': [0, 0, 0, 0, 1, 0, 0],
                    'rcb': [0, 0, 0, 0, 0, 1, 0],
                    'srh': [0, 0, 0, 0, 0, 0, 1]
                }
                return switcher.get(choice, "Invalid option selected")

            array = (teams_to_onehot(batting_team)+teams_to_onehot(bowling_team))
            
            #Convert to vector suitable for model
            array.extend([score_10, wicket_10])
            result = f"\n THE PREDICTED SCORE IS: {int(model.predict([array]).squeeze())}"

            if batting_team==bowling_team:
                result= "Error!! You cannot select same team at once"
            elif wicket_10>10:
                result = "Error!! Wickets cannot exceed 10"
            return render_template('result.html', result=result)

        except:
            result = "Please select all items correctly!"
            return render_template('result.html', result=result)

        

if __name__ == "__main__":
    app.run(debug=True)
