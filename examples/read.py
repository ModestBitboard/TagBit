from tagbit import Reader

reader = Reader()

tag = reader.get_tag()

for record in tag.read():
    print(record)
