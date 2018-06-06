import feedparser

import csv


if __name__ == '__main__':

    csv_file = open("baidunews.csv", "w", newline='', encoding='gb18030')
    writer = csv.writer(csv_file)
    writer.writerow(['title', 'content'])

    url = 'https://news.baidu.com/?cmd=4&class=lishi&tn=rss'
    one_page_dict = feedparser.parse(url)

    print(one_page_dict)
    '''
    解析得到的是一个字典
    '''

    print(one_page_dict['feed'])

    
    for artilce in one_page_dict['entries']:
        print(artilce['title'])
        print('\n')
        print(artilce['summary'])
        print('\n')
        writer.writerow([artilce['title'], artilce['summary']])


