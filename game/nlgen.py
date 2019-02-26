def nllist(items):
    nlist = ""
    if items:
        for item in items[:-1]:
            nlist += item + ', '
        if len(items) > 1:
            nlist += 'and ' + items[-1]
        else:
            nlist += items[0]
    return nlist


def nlitemlist(items):
    itemlist = ""
    if items:
        for item in items[:-1]:
            itemlist += item.article + ' ' + item.name + ', '
        if len(items) > 1:
            itemlist += 'and ' + items[-1].article + ' ' + items[-1].name
        else:
            itemlist += items[0].name
    return itemlist

