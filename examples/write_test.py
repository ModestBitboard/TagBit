from tagbit import Reader
import ndef

records = [
    ndef.TextRecord("Hello, world!", 'en'),
]

reader = Reader()

tag = reader.get_tag()

tag.write(records)
