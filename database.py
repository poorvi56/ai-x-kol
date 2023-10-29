import requests
from bs4 import BeautifulSoup
import urllib3
import pdb
import time
import os


urllib3.disable_warnings()

class YarnBrand(object):
    def __init__(self, name, brand_url):
        self.name = name
        self.url = brand_url
        self.subBrands = list()
        self.download_success = True

    def add_subBrand(self, sub_brand_name):
        self.subBrands.append(sub_brand_name)

    def __str__(self):
        output = list()
        for sub_brand in self.subBrands:
            output.append(f"{self.name},{sub_brand}")
        return "\n".join(output)

    def __repr__(self):
        output = list()
        for sub_brand in self.subBrands:
            output.append(f"{self.name},{sub_brand}")
        return "\n".join(output)


def get_mainbrand_links(main_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    dest = list()
    try:
        response = requests.get(main_url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        mydivs = soup.find_all("div", {"class": "brandName"})

        for div in mydivs:
            nlink = div.a['href']
            name = div.a.string
            brand = YarnBrand(name, main_url + "/" + nlink.split("/")[-1])
            dest.append(brand)
    except:
        print("Failed to download main brands")
    return dest

def download_brand_info(brands):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    for brand in brands:
        try:
            res = requests.get(brand.url, headers=headers, verify=False)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                mdiv = soup.find_all("div", {"class": "yarn"})
                print(f"Main Brand {brand.name}, found {len(mdiv)} sub-brands")
                for div1 in mdiv:
                    brand.add_subBrand(div1.a.string)
            else:
                print("Failed to fetch data from URL", brand.url, res.status_code)
        except:
            brand.download_success = False
            print(f"Failed to process {brand.name} - sleep now")
            time.sleep(30)
    return

if __name__ == "__main__":
    url = "https://yarnsub.com/yarns"

    print("Downloading available yarn brand information")
    brands = get_mainbrand_links(url)
    print(f"Found {len(brands)} brands - download sub-brand information for each")
    download_brand_info(brands)
    print("Writing to file...")

    with open(os.path.join('db, 'brand_list.txt'), 'w', encoding='utf-8') as f:
        for yarn in brands:
            if yarn.download_success:
                f.write(f"{yarn}")

    with open(os.path.join('db', 'failed_brand_list.txt'), 'w', encoding='utf-8') as f:
        for yarn in brands:
            if not yarn.download_success:
                f.write(f"{yarn}")
