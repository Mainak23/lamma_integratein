
import os
from pdf2image import convert_from_path
import ollama
import json
import hashlib
from datetime import datetime
import shutil


model= 'llama3.2-vision'

class directory_oparation():
    def __init__(self,username, api_key,source_path):
        self.username=username
        self.api_key=api_key
        self.genarate_unique_key=self.genarate_unique_key()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.sourse_path=source_path
        self.upload_folder=os.path.join( self.script_dir,f"upload_folder_{self.genarate_unique_key}")
        self.convert_folder=os.path.join( self.script_dir,f"convert_folder_{self.genarate_unique_key}")


    def generate_unique_id(self):
        combined_input = f"{self.username}{self.api_key}"
        hash_digest = hashlib.md5(combined_input.encode()).hexdigest()
        unique_part = hash_digest[:4]
        date_time_part = datetime.now().strftime("%H%M")[-2:]
        unique_id = f"{unique_part}{date_time_part}"
        return unique_id
    
    def move_file(self):
        if not os.path.isfile(self.sourse_path):
            raise FileNotFoundError(f"The source file '{self.sourse_path}' does not exist.")
        file_name = os.path.basename(self.sourse_path)
        destination_path = os.path.join(self.upload_folder, file_name)
        shutil.move(self.sourse_path, destination_path)
        return destination_path


    def create_folder(self):
        os.makedirs(self.upload_folder,exist_ok=True)
        os.makedirs(self.convert_folder,exist_ok=True)
        print("all files created ")
    
    def Convert_pdf_to_image(self, pdf_file):
        for pdf_file in os.listdir(self.upload_folder):
            if pdf_file.endswith('.pdf'):  # Check if the file is a PDF
                pdf_path = os.path.join(self.upload_folder, pdf_file)
                images = convert_from_path(pdf_path)
                for page_num, image in enumerate(images):
                    output_filename = f"{os.path.splitext(pdf_file)[0]}_page_{page_num + 1}.png"
                    output_path = os.path.join(self.convert_folder, output_filename)
                    image.save(output_path, 'PNG')
                    print(f"Saved: {output_path}")


    def delete_files_in_directory(self):
        walk_upload = os.walk(self.upload_folder)
        walk_convert= os.walk(self.convert_folder)
        try:
            for (root1, _, files1), (root2, _, files2) in zip(walk_upload, walk_convert):
                for file1 in files1:
                    os.remove(os.path.join(root1, file1))
                    print(f"Removed: {os.path.join(root1, file1)}")
                for file2 in files2:
                    os.remove(os.path.join(root2, file2))
                    print(f"Removed: {os.path.join(root2, file2)}")
        except Exception as e:
            print(f"Error deleting files: {e}")
            
class read_file():
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.promt_path=os.path.join( self.script_dir,"promt_v2.txt")
        self.file_content = open(self.promt_path, "r").read()
        self.content=self.file_content
        self.user="user"
        self.model= model

    def result_ollama(self,input_file):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': self.user,
                    'content': self.content,  # Ensure 'content' is defined elsewhere in your code
                    'images': [input_file]
                }
            ]
        )
        table_data = response.get('message', {}).get('content', None)
        return table_data
    


def result(username,api_key,source_path):
    make_obj_preprocess=directory_oparation(username,api_key,source_path)
    make_obj_detection=read_file()
    make_obj_preprocess.create_folder()
    make_obj_preprocess.move_file()
    [make_obj_preprocess.Convert_pdf_to_image(pdf_file) for pdf_file in os.listdir(make_obj_preprocess.upload_folder)]
    image_path=[os.path.join(make_obj_preprocess.convert_folder,path) for path in os.listdir(make_obj_preprocess.convert_folder)]
    result={}
    i=0
    for image in image_path:
        result["page"]=f"page_{i}",
        result["extracted_text"]=make_obj_detection.result_ollama(image)
        i=i+1
    json_data = json.dumps(result, indent=4)
    make_obj_preprocess.delete_files_in_directory
    return print(json_data)







if __name__ == "__main__":
    user_=input("Enter your username: ")
    api_key=input("Enter your 16-character API key: ")
    file_path=input("file_path: ")
    result(user_,api_key,file_path)