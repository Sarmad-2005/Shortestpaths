# Pakistan Route Planner

A practical route planning application that finds the shortest path between cities in Pakistan using Dijkstra's Algorithm.

## Project Overview

This project demonstrates the application of graph algorithms to solve real-world routing problems. It consists of three main phases:

1. **Data Preparation**: Filter and clean city data for Pakistan
2. **Algorithm Implementation**: Build a graph and implement Dijkstra's algorithm
3. **Web Interface**: Create a user-friendly Streamlit application

## Features

- ✅ Filters Pakistani cities from a global dataset
- ✅ Calculates real distances using Haversine formula (great-circle distance)
- ✅ Implements Dijkstra's algorithm from scratch with optimized graph connectivity
- ✅ Interactive web interface with dropdown menus
- ✅ Displays shortest path with multiple intermediate cities
- ✅ **Tabular visualization**: Shows all cities in the route with step-by-step distances
- ✅ **Graphical map visualization**: Interactive map showing the route path
- ✅ Shows total distance and cumulative distance at each step

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pandas` - for data manipulation
- `streamlit` - for the web interface
- `plotly` - for interactive map visualizations

### Step 2: Prepare the Data

Run the data preparation script to filter Pakistani cities:

```bash
python data_preparation.py
```

This will create `pak_cities.csv` containing only Pakistani cities with their coordinates.

### Step 3: Run the Application

Launch the Streamlit web app:

```bash
streamlit run app.py
```

The application will open in your default web browser (usually at http://localhost:8501).

## Project Structure

```
Algoproject/
│
├── simplemaps_worldcities_basicv1.901/
│   ├── worldcities.csv          # Original dataset
│   └── license.txt
│worldcities.csv              # Copy in root for easy access
├── data_preparation.py          # Phase 1: Data filtering
├── dijkstra_algorithm.py        # Phase 2: Algorithm implementation
├── app.py                       # Phase 3: Streamlit web interface
├── test_routes.py               # Testing script for multiple routes
├── distancecalculate.py         # Helper: Distance calculation (reference)
├── adjacencyfindingcode.py      # Helper: Graph building (reference)
│
├── pak_cities.csv               # Generated: Filtered Pakistani cities
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── AI_Prompt_Log.md             # AI collaboration documentationpendencies
└── README.md                    # This file
```

## Usage

1. **Select Source Ci
   - **Route Display**: See the complete path (e.g., Lahore → Sahiwal → Gahi Mammar → ... → Karachi)
   - **Tabular View**: Detailed table showing all cities with coordinates, distance from previous city, and cumulative distance
   - **Graphical View**: Interactive map with green line showing the shortest path
     - Blue circle (●) marks the start city
     - Green diamonds (◆) mark all intermediate cities
     - Orange square (■) marks the destination city dropdown
2. **Select Destination City**: Choose your ending city from the dropdown
3. **Calculate**: Click the "Calculate Shortest Route" button
4. **View Results**: See the shortest path and total distance

## Algorithm Details

### Dijkstra's Algorithm


### Graph Connectivity

To ensure realistic routing with intermediate cities:
- Cities are only connected if they are within **200km** of each other
- This creates a more realistic road network requiring travel through multiple cities
- Total graph has **277 cities** and approximately **7,750 edges**
- Example: Lahore → Karachi goes through 8 cities (Lahore → Sahiwal → Gahi Mammar → Liaquatpur → Mirpur Mathelo → Thari Mir Wah → Sehwan → Karachi)
The core of this project is Dijkstra's shortest path algorithm, which:

1. Maintains a priority queue of cities to visit
2. Tracks the shortest known distance to each city
3. Explores cities in order of their distance from the source
4. Updates distances when shorter paths are found
5. Reconstructs the optimal path once the destination is reached

**Time Complexity**: O((V + E) log V) where V is the number of cities and E is the number of edges

### Distance Calculation

Distances are calculated using the **Haversine formula**, which computes the great-circle distance between two points on Earth given their latitude and longitude coordinates.

## Testing the Individual Components

### Test Data Preparation
```bash
pytExample Routes

When tested, the application shows multiple intermediate cities:

- **Lahore → Karachi**: 8 cities, 1045.04 km
- **Islamabad → Multan**: 5 cities, 418.59 km  
- **Peshawar → Quetta**: 6 cities, 627.04 km
- **Rawalpindi → Gwadar**: 11 cities, 1411.03 km

## Future Enhancements

- ✅ ~~Add visualization of the route on a map~~ (Completed with Plotly)
- Include time estimates based on average travel speeds
- Support for multiple route preferences (fastest vs shortest)
- Export route to different formats
- Add traffic conditions and road quality factor
python dijkstra_algorithm.py
```
Output: Sample shortest path calculation

## AI Collaboration

This project was developed with assistance from AI tools. All prompts and interactions are documented separately as required.

## Future Enhancements

- Add visualization of the route on a map
- Include time estimates based on average travel speeds
- Support for multiple route preferences (fastest vs shortest)
- Export route to different formats

## License

This project uses data from SimpleMaps. Please refer to `simplemaps_worldcities_basicv1.901/license.txt` for data usage terms.

## Author

Created as part of a computer science practical project demonstrating graph algorithms and software development skills.
