# %%
import pandas as pd
from urllib import request, error
import re
import string

# %%

def read_book(book_id):
    target_url = f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt'
    backup_url = f'https://www.gutenberg.org/files/{book_id}/{book_id}.txt'
    
    # Adding User-Agent and Accept headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,text/plain;q=0.9,*/*;q=0.8'
    }

    req = request.Request(target_url, headers=headers)

    try:
        response = request.urlopen(req)
        print(book_id)
        x = response.read().decode('utf-8')  # Assuming the text is encoded in UTF-8
        
    # Use back up URL for 404
    except error.HTTPError as e:        
        if e.code == 404:
 
            req = request.Request(backup_url, headers=headers)
    
            try:
                response = request.urlopen(req)
                x = response.read().decode('latin1')  # Assuming the text is encoded in UTF-8   
                print(book_id,'backup')
            
            except error.HTTPError as e:
                x = None
                print(book_id,'no book found')
    
        x = None
    except Exception as e:
        print(f"An error occurred: {e}")
        x = None


    return x

def remove_punctuation(input_string):
    
    # Create a translation table to replace punctuation with spaces
    translation_table = str.maketrans({char: ' ' for char in string.punctuation if char != '-'})
    
    # Apply the translation
    modified_string = input_string.translate(translation_table)
    
    # Remove "chapter"
    modified_string = modified_string.replace('Chapter','')
    modified_string = modified_string.replace('CHAPTER','')
    
    # replace multiple spaces with a single space
    modified_string = ' '.join(modified_string.split())
    
    return modified_string


# Clean for analysis
def parse_book(txt):
    if 'START OF THE PROJECT GUTENBERG EBOOK ' in txt:
        txt = txt.split('START OF THE PROJECT GUTENBERG EBOOK ')[1]
    elif 'START OF THIS PROJECT GUTENBERG EBOOK ' in txt:
        txt = txt.split('START OF THIS PROJECT GUTENBERG EBOOK ')[1]
        
    if '*** END OF THE PROJECT GUTENBERG EBOOK ' in txt:
        txt = txt.split('*** END OF THE PROJECT GUTENBERG EBOOK ')[0]
        
    
    txt = remove_punctuation(txt).lower()
    txt = txt.split(' ')
    return txt
    
def analyze(txt_list):
    running_uniques = []
    n = 0
    seen = set()
    for word in txt_list:
        if word not in seen:
            n += 1
            seen.add(word)
        running_uniques.append(n)

    return running_uniques

def run_all(row):
    book_id, book_name, author = row['Text#'], row['Title'], row['Authors']
    
    txt = read_book(book_id)
    
    if txt != None:
    
        txt_list = parse_book(txt)
        uniques = analyze(txt_list)

    else:
        
        print('error','book_id')
        uniques = []

    return uniques

# %%
# Open the file
df = pd.read_csv('assets/pg_catalog.csv')

# Filter to certain authors
authors_list = ["Austen, Jane", "Dostoyevsky, Fyodor", "Hawthorne, Nathaniel"]
pattern = '|'.join(authors_list)
filtered_df = df[df['Authors'].str.contains(pattern,na=False)]

# Filter to fiction in English
filtered_df = filtered_df[filtered_df['Subjects'].str.contains('Fiction',na=False,case=False)]
filtered_df = filtered_df[~filtered_df['Subjects'].str.contains('Short',na=False,case=False)]
filtered_df = filtered_df[filtered_df['Language'] == 'en']
filtered_df = filtered_df[filtered_df['Type'] == 'Text']

# %%
filtered_df['result'] = filtered_df.apply(run_all, axis=1)


# %%
filtered_df = filtered_df[filtered_df['result'].apply(lambda x: len(x)) > 0]

# %%
filtered_df.to_csv('assets/parsed_books.csv',index=False)

# %%



