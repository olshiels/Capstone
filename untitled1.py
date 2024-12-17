#Your Python script should carry out the following steps:
#1. read in your current list of enhancer regions
#2. for each entry extract the chromosome and start- and end-coordinate
#3. submit these to the PFPE interface
#4. retrieve a response from the server
#5. extract URL of job webpage
#6. add this to the list of enhancer regions

#verifying that i can access bioinf.gen.tcd.ie
import requests

url = "https://bioinf.gen.tcd.ie"
try:
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully accessed {url}")
    else:
        print(f"Failed to access {url}, Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error accessing {url}: {e}")

import requests

# Step 1; read the tab-delimited file and extract the enhancer regions
def read_enhancer_file(file_path):
    enhancer_regions = []
    with open(file_path, 'r') as f:
        next(f) #ignore the headers
        for line in f:

            #Step 2; split each line by tab to get chromosome, start, and end
            fields = line.strip().split("\t")
            chromosome = fields[1]
            start = fields[2]
            end = fields[3]
            enhancer_regions.append((chromosome, start, end))
    return enhancer_regions

#for easy access of my files
from google.colab import drive
drive.mount('/content/drive')

#verification of steps 1 and 2
read_enhancer_file("/content/drive/MyDrive/CAP PYTHON.txt")

# Step 3; construct the URL for the PFPE submission
def construct_submission_url(chromosome, start, end):
    url = f"https://bioinf.gen.tcd.ie/cgi-bin/pfpe/pfpe_wrapper.pl?chr_abs={chromosome}&us_coord_abs={start}&ds_coord_abs={end}&submit=Submit+coordinates"
    return url

import re #needed for next cell

# Step 3-5?; to submit the request to PFPE interface and retrieve the response
def submit_to_pfpe_interface(url):
    response = requests.get(url)

    if response.status_code == 200:
       m = re.search('<!-- URL (https.+?) -->', response.text)

       if m:
           job_url = m.group(1)
           print("Job URL:", job_url)
       else:
           print("No job URL found in the response.")

# Step 6; update enhancer list with new data
def update_enhancer_list_with_url(enhancer_regions, file_path):
    with open(file_path, 'a') as f:
        for enhancer in enhancer_regions:
            chromosome, start, end = enhancer

            url = construct_submission_url(chromosome, start, end)

            response_text = submit_to_pfpe_interface(url)

            if response_text:
                job_url = extract_job_url(response_text)
                if job_url:
                    f.write(f"{chromosome}\t{start}\t{end}\t{job_url}\n")
                else:
                    print(f"No job URL found for {chromosome}:{start}-{end}")
            else:
                print(f"Failed to submit for {chromosome}:{start}-{end}")

def main():
    input_file = '/content/drive/MyDrive/CAP PYTHON.txt'
    output_file = '/content/drive/MyDrive/CAP RESULTS.txt'

    enhancer_regions = read_enhancer_file(input_file)

    update_enhancer_list_with_url(enhancer_regions, output_file)

if __name__ == "__main__":
    main()

