from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/trainModel")
def trainModel():
    # Check if the model name hash matches with the local database hash model through an API
    # if not, then claim the new model through the API again
    # train the model iteratively locally and store the model's training weights and bias' in the database
    return redirect(url_for("homePage"))
@app.route("/sendModel")
def sendModel():
    # Check if the model name hash matches with the local database hash model through an API
    # If no, then prompt user to claim a new model and train it first
    # If yes, then query from the local/cloud database and then send the model over to the server through the API
    return redirect(url_for("homePage"))

@app.route("/predict")
def prediction():
    # Get the prediction from the locally trained model
    # and then direct to the prediction page or render some javascript idk as an overlay
    return redirect(url_for("homePage"))
if __name__ == "__main__":
    app.run(debug=True)