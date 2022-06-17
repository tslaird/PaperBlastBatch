



import urllib
import pandas as pd
import os
from bs4 import BeautifulSoup as bs


class MyHTMLParser(HTMLParser):
   #Initializing lists
   lsStartTags = list()
   lsEndTags = list()
   lsStartEndTags = list()
   lsComments = list()

   #HTML Parser Methods
   def handle_starttag(self, startTag, attrs):
       self.lsStartTags.append(startTag)

   def handle_endtag(self, endTag):
       self.lsEndTags.append(endTag)

   def handle_startendtag(self,startendTag, attrs):
       self.lsStartEndTags.append(startendTag)

   def handle_comment(self,data):
       self.lsComments.append(data)

#creating an object of the overridden class
parser = MyHTMLParser()
parser.feed(str(data))
print("Start tags", parser.lsStartTags)
print(parser.lsEndTags)


soup = bs(data) 
soup.findAll('p')[2]

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
    soup = bs(data) 
    count= str(soup.findAll('p')[2]
    result_list.append([name,protein,'=HYPERLINK("'+'file://' +working_dir+'/'+name+'.html'+'")','=HYPERLINK("'+path+'")', ] )
    
    
results_df=pd.DataFrame(result_list,columns=['Name','Sequence','Search_path','Local_filepath'])   
results_df.to_excel('paper_blast_output.xlsx')
   
print(time.time() -start)
