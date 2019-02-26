def nllist(items):
    nlist = ""
    print(items)
    print(items[0])
    print(len(items))
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
            itemlist += item.article + item.name + ', '
        itemlist += 'and ' + items[-1].article + items[-1].name
    return itemlist

