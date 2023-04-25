from itertools import permutations

from .algorithm import algorithm


# Define a melhor ordem para passar pelas dungeons
def set_best_order(start, points, maps):

    # Pontos de referência
    dungeons = [points[f'dungeon_{i}'] for i in range(1, 4)]
    end = points['entrada_lost_woods']

    # Obtem o melhor caminho entre os pontos de referência
    paths = {}
    for i in range(len(dungeons)):
        paths[f'start-dungeon_{i+1}'] = algorithm(
            maps, maps.get_node(start),
            maps.get_node(dungeons[i])
        )
        paths[f'dungeon_{i+1}-entrada_lost_woods'] = algorithm(
            maps, maps.get_node(dungeons[i]),
            maps.get_node(end)
        )
        for j in range(i+1, len(dungeons)):
            paths[f'dungeon_{i+1}-dungeon_{j+1}'] = algorithm(
                maps, maps.get_node(dungeons[i]),
                maps.get_node(dungeons[j])
            )
            paths[f'dungeon_{j+1}-dungeon_{i+1}'] = list(
                reversed(paths[f'dungeon_{i+1}-dungeon_{j+1}'])
            )

    print('\n----------------------------------------------- CUSTOS ----------------------------------------------\n')

    # Calcula os custos para cada caminho
    costs = {}
    for key, nodes in paths.items():
        path_cost = sum(list(map(lambda node: node.cost, nodes)))
        costs[key] = path_cost - nodes[-1].cost
        (start_name, end_name) = key.split("-")
        start_name = '{:9}'.format(start_name)
        print(f'cost: {costs[key]}, path: {start_name} --> {end_name}')

    # Lista todas as ordens de caminhos possíveis
    permuts = list(permutations(['dungeon_1', 'dungeon_2', 'dungeon_3']))
    orders = list(map(
        lambda order: ['start'] + list(order) + ['entrada_lost_woods'],
        permuts
    ))

    # Soma os custos para todas as ordens de caminhos possíveis
    # e verifica a melhor ordem de caminho entre as dungeons
    order_paths = []
    best_cost = float("inf")
    best_order_path_index = 0

    for index, order in enumerate(orders):
        total_cost = 0

        for i in range(len(order)-1):
            total_cost += costs[f'{order[i]}-{order[i+1]}']

        order_paths.append({
            'total_cost': total_cost,
            'order': order
        })

        if total_cost < best_cost:
            best_cost = total_cost
            best_order_path_index = index

    print('\n---------------------------------- MELHOR CAMINHO ENTRE AS DUNGEONS ---------------------------------\n')
    print(order_paths[best_order_path_index])

    best_order = orders[best_order_path_index].copy()

    # Seleciona os paths da melhor ordem de caminho entre as dungeons
    best_order_path = order_paths[best_order_path_index]['order']
    best_paths = []
    for i in range(len(best_order_path)-1):
        best_paths.append(
            paths[f'{best_order_path[i]}-{best_order_path[i+1]}'])

    # Define o order path e o primeiro end point do mapa
    path = best_paths
    current_path = path.pop(0)

    order = order_paths[best_order_path_index]['order']
    current_order = (order.pop(0), order[0])

    maps.end_point = points[order[0]]
    maps.set_end_node()

    print('\n------------------------------------------ OUTROS CAMINHOS ------------------------------------------\n')
    for i in range(len(order_paths)):
        if i != best_order_path_index:
            print(order_paths[i], end='\n\n')

    print('\n----------------------------------------- CAMINHO PERCORRIDO -----------------------------------------\n')
    (start, end) = current_order
    print(
        f'\rtotal_cost: 0, cost: 0, {start} --> {end}', end='')

    return {
        'best_order': best_order,
        'path': path,
        'current_path': current_path,
        'order': order,
        'current_order': current_order,
        'current_end_point': maps.end_point
    }
