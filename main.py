from flask import Flask, render_template
import os, cv2
from flask import Flask, flash, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r"C:\Users\jaish\OneDrive\Desktop\git\Image Editor\uploads"
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'cgray', 'webp'}


app =Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# code for converting to desired type 
def processImage(operation, filename):
    print (f"The Operation name is {operation} and filename is {filename}")
    img = cv2.imread(fr"C:\Users\jaish\OneDrive\Desktop\git\Image Editor\uploads\{filename}")
    match operation:
        case "cgray":
            imgprocessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(fr"C:/Users/jaish/OneDrive/Desktop/git/Image%20Editor/static/{filename}",imgprocessed)






@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods = ["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "error no selescted file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImage(operation,filename)
            # for flashing end link for converted file
            flash(fr"Your file has been converted click <a href='file:///C:/Users/jaish/OneDrive/Desktop/git/Image%20Editor/static/{filename}'>here</a>")
            return render_template("index.html")
            
        
    return render_template("index.html")


app.run(debug=True, port=5002)