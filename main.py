import requests
import re
import os

DATA_FOLDER = 'data'
if not os.path.isdir(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

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

    all_links = re.findall('\[\[(.*?)\]\]', text)

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
    # reading the local cache
    local_path = build_local_path(url_link)
    if os.path.exists(local_path):
        print('reading from chache')
        return read_local(local_path)
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
        save_local(local_path, text)
        return text
    else:
        return None

def build_local_path(url_link, folder=DATA_FOLDER):
    return os.path.join(DATA_FOLDER, url_link)

def save_local(path, text):
    with open(path, 'wt') as fp:
        fp.write(text)

def read_local(path):
    with open(path, 'rt') as fp:
        text = fp.read()
    return text

def format_link(link):
    'properly format link to create a valid wikipedia url'
    return link.rstrip().replace(" ", "_")


if __name__ == '__main__':
    all_links = map(clean_link, find_links('raw.md', local=True, total=False))
    #print(list(all_links)[2:3])
    this = {k: find_links(k) for k in list(all_links)[:5] if k and find_links(k)}
    #print(len(this))
    #save_local(build_local_path('aaaa'), 'this is the betx\nasokdjaoksdjaslkd\n')
    #check_link('Algorithm')
    #this = list(map(check_link, all_links[:12]))
    #print(this)
    #that = [connect(l) for l in this]
    #print(that)
    #connect('Hopcroft–Karp_Algorithm')
