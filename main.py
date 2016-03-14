import requests
import re

ROOT = "https://en.wikipedia.org/w/index.php?title={}&action=raw"

def find_links(page, local=False, total=True):
    if not page:
        return None
    if local:
        with open(page, 'r') as fp:
            text = fp.read()
    else:
        text = connect(page)
        if not text:
            return

    all_links = re.findall('\[\[(.*?)\]\]', text)[:20]

    if total:
        return len(all_links)
    else:
        return all_links

def clean_link(link):

    if "#" in link:
        # this specific algo seem not to have a page for itlsef, so we can skip that
        return None
    if "|" not in link:
        # there is no alternate name in the link
        url_link = format_link(link)
    if "|" in link:
        # a wiki link has the following strucutre:
        # actual link | name_on_screen
        # so we are inteested in the actual link only
        link_parts = link.split("|")
        try:
            assert len(link_parts) == 2
        except AssertionError:
            # log the error
            return None
        url_link = format_link(link_parts[0])
    return url_link

def connect(url_link):
    redirect = True
    try:
        while redirect and url_link:

            #print("URL LINK ", url_link)
            r = requests.get(ROOT.format(url_link))
            #print(ROOT.format(url_link))
            if r.status_code is not 200:
                # note: s
                raise requests.ConnectionError
            #print("!!!!!!!")
            text = r.text
            if text.startswith("#REDIRECT"):
                #print(text, )
                url_link = clean_link(re.findall('\[\[(.*?)\]\]', text)[0])

            else:
                redirect = False
            # redirect
    except requests.ConnectionError:
        print("@@@@@", url_link)
            #log the eroor?
        return None
    #print(text)
    if url_link:
    #print('usciti con ', url_link)
        return text
    else:
        return None

def format_link(link):
    'properly format link to create a valid wikipedia url'

    return link.rstrip().replace(" ", "_")


if __name__ == '__main__':
    all_links = map(clean_link, find_links('raw.md', local=True, total=False))
    #print(list(all_links)[2:3])
    this = {k: find_links(k) for k in list(all_links)[2:3] if k and find_links(k)}
    print(this)
    #check_link('Algorithm')
    #this = list(map(check_link, all_links[:12]))
    #print(this)
    #that = [connect(l) for l in this]
    #print(that)
    #connect('Hopcroft–Karp_Algorithm')
