from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl


def add_query_params(url, params):
    # Parse the URL
    url_parts = list(urlparse(url))

    # Convert existing query parameters into a dictionary
    query = dict(parse_qsl(url_parts[4]))

    # Update the query parameters with the new ones
    query.update(params)

    # Encode the updated query parameters and add them back to the URL
    url_parts[4] = urlencode(query)

    # Return the modified URL
    return urlunparse(url_parts)
