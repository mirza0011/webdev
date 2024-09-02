import csv
import os
import requests

def download_images_from_csv(csv_file_path, output_folder):
    # Create the directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the CSV file and read its content
    with open(csv_file_path, mode='r', newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row if there is one
        
        for row in reader:
            if len(row) < 2:
                continue  # Skip rows that don't contain at least two columns
            title, image_url = row[0], row[1]
            title = title.replace(' ', '_')  # Replace spaces with underscores
            try:
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    filename = f"{title}.jpg"
                    filepath = os.path.join(output_folder, filename)
                    with open(filepath, 'wb') as img_file:
                        for chunk in response.iter_content(1024):
                            img_file.write(chunk)
                    
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download image from {image_url}")
            except Exception as e:
                print(f"Error downloading {image_url}: {e}")

if __name__ == "__main__":
    # Define the input CSV file path and output folder
    csv_file_path = 'downloadinput.csv'  # Change this to the path of your CSV file
    output_folder = 'featured_images'
    
    # Call the function to download images
    download_images_from_csv(csv_file_path, output_folder)