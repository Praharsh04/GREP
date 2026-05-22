content = open('sample_q_tc_raw.html', encoding='utf-8').read()
index = content.lower().find('correct')
while index != -1:
    print(f"Match at {index}:")
    print(content[index-50:index+150].replace('\n', ' '))
    index = content.lower().find('correct', index + 1)
