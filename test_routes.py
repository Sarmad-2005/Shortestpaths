from dijkstra_algorithm import CityGraph

print('Building graph with 200km connections...\n')
graph = CityGraph('pak_cities.csv')
total_edges = sum(len(neighbors) for neighbors in graph.adjacency.values()) // 2
print(f'Total edges: {total_edges}\n')

tests = [
    ('Lahore', 'Karachi'),
    ('Islamabad', 'Multan'),
    ('Peshawar', 'Quetta'),
    ('Faisalabad', 'Hyderabad'),
    ('Rawalpindi', 'Gwadar')
]

for src, dst in tests:
    path, dist = graph.dijkstra(src, dst)
    if path:
        print(f'{src} -> {dst}:')
        print(f'  Cities: {len(path)}')
        print(f'  Path: {" -> ".join(path)}')
        print(f'  Distance: {dist:.2f} km\n')
    else:
        print(f'{src} -> {dst}: No path found!\n')
