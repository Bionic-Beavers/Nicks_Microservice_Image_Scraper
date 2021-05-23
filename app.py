# Adapted from  https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/  and 
# https://www.w3resource.com/python-exercises/web-scraping/web-scraping-exercise-8.php 


from flask import Flask, render_template, json, request, redirect

import database.db_connector as db

import os

import wikipedia


# Configuration

app = Flask(__name__)
port = int(os.environ.get('PORT', 8545))

db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():

    query = request.args.get('q')
    defaultPage = "Puppies"
    
    try: 
        # Get page from wikipedia based on search query
        wikiPage = wikipedia.page(title=query, auto_suggest=False)
        print("Exact Page Found. Checking for images from page")
    except:
        try:
            print("No exact match. Using auto-suggest feature.")
            wikiPage = wikipedia.page(title=query, auto_suggest=True)
        except:
            print("No page found. Using default image.")
            # Manually set the default image by specifying a page
            wikiPage = wikipedia.page(defaultPage)
    

    # Get list of images from current Wikipage using API
    images = wikiPage.images
    print(images)
    #Initialize variable
    imagePath = ''

    try: 
        # Get the last jpg image in the list (as this is the topmost jpg image on the wikiPage)
        for i in range(len(images) - 1, 0, -1):
            fileType = images[i][(len(images[i])-3):len(images[i])]
            if fileType.lower() == "jpg":
                imagePath = images[i]
                print("Image found. Path: ", imagePath)
                break
    except: 
        imagePath = ("http://flip3.engr.oregonstate.edu:" + str(port) + "/?q=" + urlify(defaultPage, len(defaultPage)))
    
    return redirect(imagePath)


def urlify(in_string, in_string_length):
    return in_string[:in_string_length].replace(' ', '%20')

# Listener 
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 8545))
    app.run(port=port, debug=True) 


