import requests
import requests, PyPDF2, io
from PyPDF2 import PdfReader  
import os
import pandas as pd
import sys
import time
import re

length = 0 
done = 0 


def main():

    global length

    df = pd.read_csv(os.path.join("data", "data.csv")).iloc[500:]
    

    length = len(df.index)

    df['text'] = df['URL'].apply(get_text)

    df.to_csv(os.path.join("data", "output.csv"))

def progress(): 
    global length
    global done

    done += 1 

    bar_length = 30
    percent = float(done) / length
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rProgress: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()



def get_text(url,save=False, recurs=False): 

    if recurs==False: 

        match = re.search(r'bill\/(\d*)[\s\S]*?senate-bill\/(\d*)', url)

        # Check if there is a match
        if match:
            # Accessing match groups
            bill_num = match.group(1)
            sen_num = match.group(2) 
        else:
            print("Could not locate bill and senate number...")
            print(url)
            return ''
        
        #creates the url for a scraping accesible database since interacting directly with database is blocked by anti scraping software
        new_url = url[0:25] + bill_num + "/bills/s" + sen_num + "/BILLS-" + bill_num + "s" + sen_num + "is.pdf"

    else: 
        new_url = url 
    
    print(new_url)

    response = requests.get(new_url, cookies=None)
    
    if response.status_code == 200: 
        with io.BytesIO(response.content) as open_pdf_file:
            full_text = ''
            reader = PdfReader(open_pdf_file)
            for page in reader.pages: 
                full_text += page.extract_text()
        
        if save: 
            with open(os.path.join("data", "testdowload.txt"), 'w') as file: 
                file.writelines(full_text)

        progress()
        return full_text
    

    #If the request fails, try with a slightly different url that may work, not sure why there are differences sometimes
    elif new_url[-6:-4] == 'is': 

        
        changed_url = new_url[:-6] + "rs" + new_url[-4:]
        return get_text(changed_url,save=False , recurs=True)
    
    elif new_url[-6:-4] == 'rs': 

        
        changed_url = new_url[:-6] + "cps" + new_url[-4:]
        return get_text(changed_url,save=False , recurs=True)

    else: 
        print("\n\nError: " + str(response.status_code) +"\n\nFrom url: " + new_url +  "...")
        return '' 
    
    

main()