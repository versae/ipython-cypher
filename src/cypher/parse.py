import os

from cypher.utils import DEFAULT_URI


def parse(cell, config):
    uri = (os.environ.get("NEO4J_URI")
           or os.environ.get("NEO4J_URL")
           or DEFAULT_URI)
    uri_as = ""
    parts = [part.strip() for part in cell.split(None, 1)]
    if not parts:
        return {'uri': uri, 'cypher': ''}
    elif ' as ' in parts[0]:
        uri, uri_as = parts[0].split(' as ')
    elif '@' in parts[0] or '://' in parts[0]:
        uri = parts[0]
        if len(parts) > 1:
            query = parts[1]
        else:
            query = ''
    else:
        query = cell
    return {'uri': uri.strip(),
            'as': uri_as.strip(),
            'cypher': query.strip()}
