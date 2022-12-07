def cut_link(link):
    link_without_http = link.replace("https://", "")
    params = link_without_http.split("/")
    return f'https://{params[0]}/{params[1]}/'


def post_from_link(link):
    link_without_http = link.replace("https://", "")
    params = link_without_http.replace(".html", "").split("/")
    return f'{params[1]}'
