from functions import *


if __name__ == "__main__":

    tweet_count = 0

    while True:

        link = ''
        tfa = False
        otd = False

        if tweet_count == 4:
            link = get_link_from_main_page('mp-tfa')
            print(link)
            tfa = True
            tweet_count += 1

        elif tweet_count == 8:
            link = get_link_from_main_page('mp-otd')
            print(link)
            otd = True
            tweet_count += 1

        elif tweet_count == 12:
            tweet_count = 0

        else:
            links = ['https://en.wikipedia.org/wiki/Special:RandomInCategory/Featured_articles',
                     'https://en.wikipedia.org/wiki/Special:Random']
            link = random.choice(links)
            tweet_count += 1

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
                tweet(img_directory, tweet)
                remove_files(json_directory, img_directory)
            else:
                print("Image is too big.")
                remove_files(json_directory, img_directory)

        except:
            print("File not found.")
            pass

