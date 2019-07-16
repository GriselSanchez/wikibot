from functions_2 import *

# Generar un artículo random dentro de una categoría:
# https://en.wikipedia.org/wiki/Special:RandomInCategory/Category

if __name__ == "__main__":
    tweet_counter = 0
    while True:
        link = ''
        tfa = False
        otd = False
        if tweet_counter == 4:  # todays featured article is the fourth tweet of the day
            link = parse_main_page('mp-tfa')
            print(link)
            tfa = True
            tweet_counter += 1

        elif tweet_counter == 8:  # on this day is the eight tweet of the day
            link = parse_main_page('mp-otd')
            print(link)
            otd = True
            tweet_counter += 1

        elif tweet_counter == 24:
            tweet_counter = 0
            continue

        else:
            links = ['https://en.wikipedia.org/wiki/Special:RandomInCategory/Featured_articles',
                     'https://en.wikipedia.org/wiki/Special:Random']
            # 'https://en.wikipedia.org/wiki/USS_Constitution' links like this dont work
            link = random.choice(links)
            tweet_counter += 1

        page_soup = parse(link)

        title = get_title(page_soup)
        link = get_final_link(title)

        page_soup = remove_unwanted_html(page_soup)
        clean_html = page_soup.findAll('div', {'class': 'mw-parser-output'})

        tweet = get_final_tweet(clean_html, link, tfa, otd)

        get_image(title)

        json_directory = get_json_directory(title)
        img_directory = get_image_directory(json_directory)

        try:
            if check_image_size(json_directory, 3072):
                # tweet(img_directory, tweet)
                remove_files(json_directory, img_directory)
            else:
                print("Imagen demasiado grande")
                remove_files(json_directory, img_directory)

        except:
            print("Archivo no localizado")
            pass


