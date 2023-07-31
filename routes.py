def routes(routes_tuple):
    routes_list = []
    for i in routes_tuple:
        i = list(i)
        i = list(map(float, i))
        routes_list.append(i)
    return routes_list
