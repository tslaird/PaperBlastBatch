



import urllib
import pandas as pd
import os
from bs4 import BeautifulSoup as bs


#creating an object of the overridden class
parser = MyHTMLParser()
parser.feed(str(data))
print("Start tags", parser.lsStartTags)
print(parser.lsEndTags)


soup = bs(data) 


with open('/home/tslaird/leveau_lab/PaperBlastBatch/iac_proteins.fasta','r') as file:
    all_proteins=file.read()
    
protein_list= ['>'+ i for i in all_proteins.split('>')[1::]]

url_head="http://papers.genomics.lbl.gov/cgi-bin/litSearch.cgi?query="


result_list=[]
working_dir=os.getcwd()
import time
start=time.time()
for protein in protein_list:
    name=protein.split('\n')[0][1::]
    protein_str=protein.replace('\n','%0D%0A')
    path=url_head+protein_str+"&Search=Search"
    html_page=urllib.request.urlretrieve(path,name+'.html')
    with urllib.request.urlopen(path) as response, open(name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)
    x=parser.feed(data))
    if re.findall('similar proteins')
    result_list.append([name,protein,'=HYPERLINK("'+'file://' +working_dir+'/'+name+'.html'+'")','=HYPERLINK("'+path+'")', ] )
    
    
results_df=pd.DataFrame(result_list,columns=['Name','Sequence','Search_path','Local_filepath'])   
results_df.to_excel('paper_blast_output.xlsx')
   
print(time.time() -start)
