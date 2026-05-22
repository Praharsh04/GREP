content = open('tc_listing_ajax.html', encoding='utf-8').read()
index = content.lower().find('sovereignty')
if index != -1:
    print(content[index-200:index+500])
else:
    print("Not found")
