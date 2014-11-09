

def parse(cell, config):
    opts, cell = config.parse_options(cell, '')

    uri = 'http://localhost:7474/db/data/'
    parts = [part.strip() for part in cell.split(None, 1)]
    if not parts:
        return {'uri': uri, 'cypher': ''}
    elif '@' in parts[0] or '://' in parts[0]:
        uri = parts[0]
        if len(parts) > 1:
            query = parts[1]
        else:
            query = ''
    else:
        query = cell
    return {'uri': uri.strip(),
            'cypher': query.strip()}
