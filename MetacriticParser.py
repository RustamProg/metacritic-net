from bs4 import BeautifulSoup
import pandas as pd
import requests

pd.set_option('display.max_columns', 10)

# 0 - positive review
# 1 - negative review
# 2 - mixed review
df = pd.DataFrame(columns=['Text', 'Score Dist'])


def parse_all_reviews(url, type, df):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    last_page_num = 30
    new_row = {}
    score_dist = 0
    if type == 0:
        score_dist = 0
    elif type == 1:
        score_dist = 1
    else:
        score_dist = 2
    for page_list in range(int(last_page_num)):
        new_url = url+'&page='+str(page_list)
        page = requests.get(new_url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        reviews = soup.find_all('div', {'class': 'review_body'})
        for elem in reviews:
            try:
                if elem.find('span')['class'][0] == 'inline_expand_collapse' or elem.find('span')['class'][0] == 'inline_expand_collapse' == 'toggle_text_visibility':
                    new_row = {'Text': elem.find('span', {'class': 'blurb blurb_expanded'}).text, 'Score Dist': score_dist}
            except BaseException:
                span_text = elem.find('span')
                if span_text == None:
                    break
                new_row = {'Text': span_text.text, 'Score Dist': score_dist}
            df = df.append(new_row, ignore_index=True)
        print(f'Идет парсинг страницы {page_list+1} из {last_page_num}')
    return df


pos_url = 'https://www.metacritic.com/game/playstation-4/the-last-of-us-part-ii/user-reviews?sort-by=date&num_items=100&dist=positive'
neg_url = 'https://www.metacritic.com/game/playstation-4/the-last-of-us-part-ii/user-reviews?sort-by=date&num_items=100&dist=negative'
mix_url = 'https://www.metacritic.com/game/playstation-4/the-last-of-us-part-ii/user-reviews?sort-by=date&num_items=100&dist=neutral'


df = parse_all_reviews(pos_url, 0, df)
df = parse_all_reviews(neg_url, 1, df)
df = parse_all_reviews(mix_url, 2, df)


print(df)
df.to_excel('reviews.xlsx', sheet_name='reviews')
df.to_csv('reviews.csv')


