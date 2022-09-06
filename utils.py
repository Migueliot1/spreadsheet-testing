def get_range(start=None, end=None, sheet_name=None):
    if not start and not end:
        _range = sheet_name
    elif not end:
        _range = f"{sheet_name}!{start}:Z"
    elif not start:
        _range = f"{sheet_name}!A:{end}"
    else:
        _range = f"{sheet_name}!{start}:{end}"

    return _range


def get_body_insert(_range, _values):
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": _range,
             "values": _values}
        ]}
    return body
