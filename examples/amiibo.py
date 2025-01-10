from tagbit import Reader

reader = Reader()

tag = reader.get_tag()

amiibo_id = tag.get_id()

print("Amiibo ID:", amiibo_id)

with open("amiibo.bin", 'wb') as f:
    f.write(tag.dump())
