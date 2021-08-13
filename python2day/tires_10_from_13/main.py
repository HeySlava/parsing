import  requests


def get_data():

    headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Is-Ajax-Request": "X-Is-Ajax-Request",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }

    url = "https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&arCatalogFilter_463=668736523&PAGEN_1=1"

    r = requests.get(url=url)

    # with open("index.html", "w") as file:
    #     file.write(r.text)

    # with open("index.html") as file:
    #     src = file.read()

    print(r.json())
    # print(src)


def main():
    get_data()


if __name__ == "__main__":
    main()

