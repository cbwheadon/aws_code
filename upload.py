import os
import subprocess

in_dir = "/home/chris/Documents/SchoolData/done/abingtonpre"
pdf_files = os.listdir(in_dir)
#for pdf in pdf_files:
pdf = pdf_files[0]
infile = os.path.join(in_dir,pdf)
print infile
print pdf.replace(".pdf","")
#create a new user

