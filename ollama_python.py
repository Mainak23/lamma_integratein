import ollama
import os
# Send the chat request to extract the table from the image


content="""As an experienced data entry operator, extract the table from the given image, including all rows and columns. Ensure you capture and list the following details:

Invoice Number/Buyer's Order Number
GST Number
Invoice Date
PO Number
Total Amount
Total Items
Total Cost
Additionally, extract the table data with the following columns:

Sl. No
Description
Code
Total
Make sure to include all line items, even if they are duplicated. Format the extracted information as follows:

Invoice Number/Buyer's Order No: AB112345
Date: 23-04-1995
GST: 921345678
Total: 34,567.89
Total Items: 3
Total Cost: 3,447,769
Table:

Sl. No	Description	Code	Total
1	Item A	A123	10
2	Item B	B456	20
3	Item A	A123	10
(Note: Include all duplicate line items as shown in the image.)"""


folder_path = "out_put_path_roni_pdf"

# Ensure the output folder exists
os.makedirs(folder_path, exist_ok=True)

# Path to input folder
path_input_folder = os.path.join(os.getcwd(), "roni_pdf")

# List of input files from the input folder
input_files = [os.path.join(path_input_folder, f) for f in os.listdir(path_input_folder)]

for input_file in input_files:
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[
            {
                'role': 'user',
                'content': content,  # Ensure 'content' is defined elsewhere in your code
                'images': [input_file]
            }
        ]
    )
    
    # Extract table data from the response
    table_data = response.get('message', {}).get('content', None)

    if table_data is not None:
        # Create an output file path based on the input file's name
        output_file = os.path.join(folder_path, f'extracted_table_image_{os.path.basename(input_file)}.txt')
        
        # Save the extracted table data to a text file
        with open(output_file, 'w') as output_file_handle:
            output_file_handle.write(table_data)
        
        print(f"Table successfully extracted and saved to '{output_file}'.")
    else:
        print(f"No table data found for {input_file}.")

# Debug: Print the full response to check its structure


