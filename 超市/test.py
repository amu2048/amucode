from flask import Flask,render_template
app =Flask(__name__)

@app.route("/",methods=["GET","POST"])
def login():
    return render_template("home1/billAdd.html")



if __name__ == '__main__':
    app.run(debug=True)











