content = open('tc_listing_ajax.html', encoding='utf-8').read()
index = content.find('id="topics"')
if index != -1:
    print(content[index:index+2000])
else:
    print("Not found")
