content = open('sample_q_tc_raw.html', encoding='utf-8').read()
index = content.lower().find('sovereignty')
if index != -1:
    print(content[index-500:index+2000])
else:
    print("Not found")
