def print_container(container):
    print('{0} items in container'.format(len(container)))
    for item in container:
        print('id: {0}, name: {1}, aliases: [{2}], type: {3}'.format(item.id, item.name, ', '.join(item.aliases), type(item)))