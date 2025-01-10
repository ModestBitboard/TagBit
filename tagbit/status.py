"""
Exceptions and such made to match APDU commands
"""

apdu_errors = {  # Most of these are copy-pasted from the PC/SC specifications.
    "62:82": "The response length is shorter than the value specified by Le.",
    "64:01": "No response from a card",
    "67:00": "Invalid length",
    "68:00": "CLA is invalid",
    "69 81": "Data In is invalid",
    "69:85": "Invalid status",
    "6A:81": "INS value is invalid",
    "6B:00": "The value of P1 and P2 is invalid.",
    "6F:00": "Unexpected error",
    "69:88": "Invalid Key Number",
    "69:89": "Invalid Key Length",
    "69:83": "Authentication failure",
    "69:86": "Invalid Key Type",
    "62:8A": "Invalid FeliCa response status",
    "69:82": "The security status is not met.",
    "6A:82": "The data at the specified address does not exist.",
    "6C:0F": "FeliCa read failed due to block upper limit set for Le.",  # I'm not familiar with FeliCa, so I might be wrong.
    "62:81": "Illegal response from card (other than FeliCa)",
    "63:8A": "FeliCa handling failure",
    "65:81": "Write failed (CRC error)",
    "6A:80": "TLV format is invalid",
    "6A:86": "P1-P2 is invalid.",
    "6A:87": "The value of Lc is inconsistent with the value of P1-P2.",
}

def raise_for_status(status: tuple[int, int]) -> None:
    """
    Raise the correct exception for the APDU status. Do nothing if successful
    """
    if status == (0x90, 0x00):
        return

    code = '{:02X}:{:02X}'.format(*status)

    if status[0] == 0x6C:
        raise TagStatusError(code + ' - Le value is invalid (Should be {:02X}h)'.format(status[1]))

    elif code in apdu_errors.keys():
        raise TagStatusError(code + ' - ' + apdu_errors[code])
    else:
        raise TagStatusError(code)

class TagStatusError(Exception):
    pass

class NoTagError(Exception):  # Just to fit the naming scheme
    pass
