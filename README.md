# TagBit
TagBit is a lightweight python library for reading and writing to NFC tags through the PC/SC API.

I built this library because [nfcpy](https://github.com/nfcpy/nfcpy) lacked support for the [Sony PaSoRi RC-S300](https://www.sony.net/Products/felica/business/products/RC-S300S1.html).
Because I built it around that device it isn't yet guaranteed to work with other readers, although since it is built around PC/SC it should have basic support for most readers.

TagBit uses [pyscard](https://github.com/LudovicRousseau/pyscard) to interface with the NFC reader.

## Installation
![PyPI](https://img.shields.io/pypi/v/tagbit)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tagbit)

You can install TagBit from [PyPI](https://pypi.org/project/tagbit) using pip.

`pip install tagbit`

## Usage
TagBit can be used to read and write NDEF messages, and to create dumps of Amiibos. Here are some examples:

### Reading
```python
from tagbit import Reader

reader = Reader()

tag = reader.get_tag()

records = tag.read()  # Returns the NDEF records from the tag.
```

### Writing
```python
from tagbit import Reader
import ndef  # https://pypi.org/project/ndeflib/

records = [
    ndef.TextRecord("Hello, world!", 'en'),
]

reader = Reader()

tag = reader.get_tag()

tag.write(records)  # Saves the NDEF records to the tag.
```

### Amiibos
```python
from tagbit import Reader

reader = Reader()

tag = reader.get_tag()

amiibo_id = tag.get_id()  # Returns the UID of the Amiibo.

amiibo_bin = tag.dump()  # Creates a dump of the Amiibo.
```

## Plans
- Add support for MIFARE Classic 1k and other formats
- Add tools for creating Amiibos from dumps
- Test with other NFC reader models and expand compatibility
- Improve NDEF implementation if needed

## Support
If you liked this project, go ahead and give it a star! And if it really helped you out, consider sending me a tip!

> **BTC**: `bc1q0pp60krluv7a2w5cls09l9ahat5lqvu7mt9efq`