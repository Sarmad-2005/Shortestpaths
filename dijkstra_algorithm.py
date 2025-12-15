"""
Phase 2: Algorithm Implementation
Build the graph of Pakistani cities and implement Dijkstra's algorithm
to find the shortest path between any two cities.
"""

import pandas as pd
import math
import heapq
from typing import Dict, List, Tuple, Optional

def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth 
    using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
    
    Returns:
        Distance in kilometers
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Compute differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    R = 6371
    
    # Calculate distance
    distance = R * c
    return distance


class CityGraph:
    """
    Graph representation of Pakistani cities with distances as edge weights.
    """
    
    def __init__(self, csv_file: str):
        """
        Initialize the graph from a CSV file containing city data.
        
        Args:
            csv_file: Path to CSV file with columns: City, Latitude, Longitude
        """
        self.cities_df = pd.read_csv(csv_file)
        self.cities = {}  # city_name -> {lat, lon}
        self.adjacency = {}  # city_name -> [(neighbor, distance), ...]
        
        # Load city coordinates
        for _, row in self.cities_df.iterrows():
            city_name = row['City']
            self.cities[city_name] = {
                'lat': row['Latitude'],
                'lon': row['Longitude']
            }
            self.adjacency[city_name] = []
        
        # Build complete graph (every city connected to every other city)
        self._build_graph()
    
    def _build_graph(self):
        """
        Build the graph by calculating distances between nearby cities only.
        This creates a more realistic road network where cities are only 
        connected to their neighbors within a certain distance threshold.
        """
        MAX_CONNECTION_DISTANCE = 200  # kilometers (balanced to ensure connectivity and intermediate cities)
        city_names = list(self.cities.keys())
        
        for i, city1 in enumerate(city_names):
            for city2 in city_names[i+1:]:
                lat1 = self.cities[city1]['lat']
                lon1 = self.cities[city1]['lon']
                lat2 = self.cities[city2]['lat']
                lon2 = self.cities[city2]['lon']
                
                distance = calculate_distance_km(lat1, lon1, lat2, lon2)
                
                # Only connect cities within the maximum distance threshold
                if distance <= MAX_CONNECTION_DISTANCE:
                    # Add edges in both directions (undirected graph)
                    self.adjacency[city1].append((city2, distance))
                    self.adjacency[city2].append((city1, distance))
    
    def get_city_names(self) -> List[str]:
        """Return sorted list of all city names."""
        return sorted(self.cities.keys())
    
    def get_all_edges(self) -> List[Tuple[str, str, float]]:
        """
        Get all edges in the graph for visualization.
        
        Returns:
            List of tuples (city1, city2, distance)
        """
        edges = []
        seen = set()
        
        for city1, neighbors in self.adjacency.items():
            for city2, distance in neighbors:
                # Avoid duplicate edges (undirected graph)
                edge_key = tuple(sorted([city1, city2]))
                if edge_key not in seen:
                    seen.add(edge_key)
                    edges.append((city1, city2, distance))
        
        return edges
    
    def dijkstra(self, source: str, destination: str) -> Tuple[Optional[List[str]], Optional[float]]:
        """
        Implement Dijkstra's algorithm to find the shortest path between two cities.
        
        Args:
            source: Name of the starting city
            destination: Name of the ending city
        
        Returns:
            Tuple of (path, distance):
                - path: List of city names in the shortest path
                - distance: Total distance in kilometers
            Returns (None, None) if no path exists
        """
        if source not in self.cities or destination not in self.cities:
            return None, None
        
        # Initialize distances with infinity
        distances = {city: float('inf') for city in self.cities}
        distances[source] = 0
        
        # Track previous city in optimal path
        previous = {city: None for city in self.cities}
        
        # Priority queue: (distance, city)
        pq = [(0, source)]
        
        # Set of visited cities
        visited = set()
        
        while pq:
            current_distance, current_city = heapq.heappop(pq)
            
            # Skip if already visited
            if current_city in visited:
                continue
            
            visited.add(current_city)
            
            # If we reached destination, we can stop
            if current_city == destination:
                break
            
            # Skip if this distance is outdated
            if current_distance > distances[current_city]:
                continue
            
            # Check all neighbors
            for neighbor, edge_distance in self.adjacency[current_city]:
                if neighbor in visited:
                    continue
                
                # Calculate new distance to neighbor
                new_distance = current_distance + edge_distance
                
                # If we found a shorter path, update it
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_city
                    heapq.heappush(pq, (new_distance, neighbor))
        
        # Reconstruct path
        if distances[destination] == float('inf'):
            return None, None  # No path found
        
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        
        return path, distances[destination]


def main():
    """
    Test the implementation with sample queries.
    """
    print("Loading Pakistani cities data...")
    graph = CityGraph('pak_cities.csv')
    
    cities = graph.get_city_names()
    print(f"\nLoaded {len(cities)} cities")
    
    # Test with example cities
    if len(cities) >= 2:
        source = cities[0]
        destination = cities[-1]
        
        print(f"\nFinding shortest path from {source} to {destination}...")
        path, distance = graph.dijkstra(source, destination)
        
        if path:
            print(f"\nShortest Path: {' → '.join(path)}")
            print(f"Total Distance: {distance:.2f} km")
        else:
            print("No path found!")


if __name__ == "__main__":
    main()
