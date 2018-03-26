import os

def parse(cell, config):
    uri = (os.environ.get("NEO4J_URI")
           or os.environ.get("NEO4J_URL")
           or config.uri)
    uri_as = ""
    parts = [part.strip() for part in cell.split(None, 1)]
    if not parts:
        return {'uri': uri, 'as': uri_as, 'cypher': ''}
    if '@' in parts[0] or '://' in parts[0]:
        uri = parts[0]
        if len(parts) > 1:
            if parts[1].startswith('as '):
                uri_as_query = parts[1].split('as', 1)[-1].split(None, 1)
                if len(uri_as_query) == 2:
                    uri_as, query = uri_as_query
                else:
                    uri_as, query = uri_as_query[0], ''
            else:
                query = parts[1]
        else:
            query = ''
    elif '$' in parts[0]:
        uri_as = parts[0][1:]
        query = parts[1]
    else:
        query = cell
    return {'uri': uri.strip(),
            'as': uri_as.strip(),
            'cypher': query.strip()}
