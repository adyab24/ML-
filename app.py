from flask import Flask, request, render_template
import os
import image_to_text
import similarity_search

app = Flask(__name__)
UPLOAD_FOLDER = r"C:\Users\prachi\OneDrive - Mahindra University\MU\Sem 4\ML\MLProject\uploads"  # Define a folder to save images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods=['GET'])
def hello_world():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'croppedImage' not in request.files:
        return 'No file part', 400
    file = request.files['croppedImage']#this is post cropping
    if file:
        filename=file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image = os.path.join(UPLOAD_FOLDER, filename)
        print("file path is:",image)
        
    response = image_to_text.image_to_text(image)
    print(response)
    if response:
        match, contents, alternatives, manu, pric = similarity_search.search_medicine(response)
        if match:
            return render_template('results.html', input=response, match=match, alternatives=alternatives, contents=contents, manufacturer=manu, price=pric)
        else:
            return "Medicine not found. Try again"   
    else:
        return "Scan unsuccessful. Retry."
    

@app.route('/find', methods=['GET']) #/find?q=ascoril
def find():
    query = request.args.get('q')
    if query:
        match, contents, alternatives, manu, pric = similarity_search.search_medicine(query)
        # print('query=', query, 'match found=', match, 'alternatives are:', alternatives)
        return render_template('find.html',input=query,match=match,alternatives=alternatives, contents=contents,manufacturer=manu,price=pric)  
    else:
        return "Medicine not found. Try again" 
if __name__ == '__main__':
    app.run(debug=True)