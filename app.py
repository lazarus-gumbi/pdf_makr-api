import os
import zipfile
from PIL import Image
from pathlib import Path
from flask_cors import CORS
from fpdf import FPDF
import glob
from flask import Flask, jsonify,request, send_file, send_from_directory

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

pdf = FPDF()


@app.route('/api/make_pdf', methods=("POST","GET"))
def make_pdf():
    # receive the zip file
    if request.method == "POST":
        scans = request.files['scans']
        scans.save(f"./{scans.filename}")
        

    # unzip the file into a folder
        with zipfile.ZipFile(f'./{scans.filename}','r') as zip_ref:
            zip_ref.extractall(f'./work_folder')
            os.remove(f"./{scans.filename}")
    # create pdf file by adding all .png and .jpg file together
        scans_list = [Image.open(item) for i in [glob.glob(f'./work_folder/{Path("./"+scans.filename).stem}/*.%s' % ext) for ext in ["jpg","gif","png","tga"]] for item in i]
        
        scans_list[0].save(
            "./pdf_makr.pdf","PDF", resolution=100.0, save_all=True, append_images=scans_list[1:]
        )
        files = glob.glob(f'./work_folder/*{Path("./"+scans.filename).stem}/*')
        for f in files:
            os.remove(f)
        os.rmdir(f'./work_folder/{Path("./"+scans.filename).stem}')
        os.rmdir('./work_folder')
        # make sure files named 1.png 2.png follow each other sequentially 
        return send_file("./pdf_makr.pdf",mimetype='pdf',download_name="pdf_makr.pdf",as_attachment=True)
    
    return send_file("./pdf_makr.pdf",mimetype='pdf',download_name="pdf_makr.pdf",as_attachment=True)

@app.route('/api/download')
def download():
    path = "./pdf_makr.pdf"   
    return send_file("./pdf_makr.pdf",mimetype='pdf',download_name="pdf_makr.pdf",as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)