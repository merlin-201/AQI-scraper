from bs4 import BeautifulSoup


def pprint(web_element):
    print(BeautifulSoup(web_element.get_attribute("outerHTML"), 'html.parser').prettify())


def ext_pprint(web_element, file_name):
    with open(f'./scraped_htmls/{file_name}.html','w',encoding='utf-8') as f:
        f.write(BeautifulSoup(web_element.get_attribute("outerHTML"), 'html.parser').prettify())

def ext_pprint_iter(web_elements, file_name):
    with open(f'./scraped_htmls/{file_name}.html','w',encoding='utf-8') as f:
        for web_element in web_elements:
            f.write('\n'+BeautifulSoup(web_element.get_attribute("outerHTML"), 'html.parser').prettify()+ '\n\n'+"="*20)

def dprint(d,indent=0):
    try:
        for key, value in d.items():
            print('\t' * indent + str(key),' : ',end="")
            if isinstance(value, dict):
                print()
                dprint(value, indent+1)
            else:
                print( str(value) )
    except:
        print("Error : Empty dict :(")