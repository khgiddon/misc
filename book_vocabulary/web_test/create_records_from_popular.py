from urllib import request, error
import re
import string
import pandas as pd


"""
Get top ebooks from Project Gutenberg
Parse data into a tuple of name, author, id

NOTE: Based on https://www.gutenberg.org HTML at URL below, 17 August 2023
"""

def get_books():
    
    response = request.urlopen("https://www.gutenberg.org/browse/scores/top")
    page_source = response.read().decode('utf-8')

    books_raw = page_source[page_source.index('Top 100 EBooks yesterday</h2>'):].split('\n')[3:103]
    books = []
    for book in books_raw:

        # Extract ID
        id_match = re.search(r'/ebooks/(\d+)', book)
        if id_match:
            book_id = int(id_match.group(1))

        # Extract name
        name_match = re.search(r'<a.*?>(.*?) by', book)
        if name_match:
            book_name = name_match.group(1).strip()
        else:
            name_match = re.search(r'<a.*?>(.*?) \(', book)
            if name_match:
                book_name = name_match.group(1).strip()

        # Extract author
        author_match = re.search(r' by (.*?) \(', book)
        if author_match:
            author = author_match.group(1).strip()
        else:
            author_match = re.search(r' by (.*?)$', book)
            if author_match:
                author = author_match.group(1).strip()
            else:
                author = ''   

        books.append((book_id,book_name,author))
        
    return books

"""
Read books and prepare for analysis
"""

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

# Get book from URL
def read_book(book_id):
    target_url = f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt'
    backup_url = f'https://www.gutenberg.org/files/{book_id}/{book_id}.txt'
    
    print(book)

    # Adding User-Agent and Accept headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,text/plain;q=0.9,*/*;q=0.8'
    }

    req = request.Request(target_url, headers=headers)

    try:
        response = request.urlopen(req)
        x = response.read().decode('latin1') 
        
    # Use back up URL for 404
    except error.HTTPError as e:
        if e.code == 404:
 
            req = request.Request(backup_url, headers=headers)
    
            try:
                response = request.urlopen(req)
                x = response.read().decode('latin1') 
                print(book,'backup')
            
            except error.HTTPError as e:
                x = None
                print(book,'no book found')
    
        x = None
    except Exception as e:
        print(f"An error occurred: {e}")
        x = None


    return x

"""
Analysis
"""

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

data = []
books = get_books()
for book in books:
    book_id, book_name, author = book
    
    txt = read_book(book_id)
    
    if txt != None:
    
        txt_list = parse_book(txt)
        uniques = analyze(txt_list)

        data.append((book,uniques))

# Novels only
novels = [
    "Moby Dick; Or, The Whale",
    "A Room with a View",
    "Middlemarch",
    "Little Women; Or, Meg, Jo, Beth, and Amy",
    "The Enchanted April",
    "Pride and Prejudice",
    "Cranford",
    "The Adventures of Roderick Random",
    "The Expedition of Humphry Clinker",
    "History of Tom Jones, a Foundling",
    "Twenty years after",
    "Frankenstein; Or, The Modern Prometheus",
    "Alice's Adventures in Wonderland",
    "Dracula",
    "The Picture of Dorian Gray",
    "Anna Karenina",
    "A Tale of Two Cities",
    "The Great Gatsby",
    "Metamorphosis",
    "The Brothers Karamazov",
    "Crime and Punishment",
    "The Scarlet Letter",
    "Ulysses",
    "The Strange Case of Dr. Jekyll and Mr. Hyde",
    "Great Expectations",
    "Jane Eyre: An Autobiography",
    "War and Peace",
    "Don Quixote",
    "Adventures of Huckleberry Finn",
    "Peter Pan",
    "The Adventures of Tom Sawyer, Complete",
    "Wuthering Heights",
    "Winnie-the-Pooh",
    "Anne of Green Gables",
    "Heart of Darkness",
    "The Wonderful Wizard of Oz",
    "Little Women",
    "Emma",
    "Treasure Island",
    "The War of the Worlds",
    "A Study in Scarlet"
]


data2 = [item for item in data if item[0][1] in novels]

# Only for books with over 100,000 words
data2 = [item for item in data2 if len(item[1]) > 100000]

# Select authors
authors = ['James Joyce','Herman Melville','E.M.  Forster','George Eliot','Louisa May Alcott','Jane Austen','Mary Wollstonecraft Shelley','Lewis Carroll','Bram Stoker','Oscar Wilde','graf Leo Tolstoy','Charles Dickens','F. Scott  Fitzgerald','Fyodor Dostoyevsky','Joseph Conrad','Mark Twain']
data2 = [item for item in data2 if item[0][2] in authors]

# Create the DataFrame

transformed_data = [{'ID': id, 'Title': title, 'Authors': author, 'result': result} 
                    for (id, title, author), result in data2]
df = pd.DataFrame(transformed_data)

df.to_csv('assets/parsed_books_popular.csv',index=False)


