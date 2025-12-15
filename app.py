
"""
Phase 3: Streamlit Web Application
A user-friendly interface for the Pakistan Route Planner.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dijkstra_algorithm import CityGraph

# Configure the page and layout
st.set_page_config(
    page_title="Pakistan Route Planner",
    page_icon="🗺️",
    layout="wide"
)

# Load graph without caching to ensure fresh data
def load_graph():
    """Load the city graph."""
    return CityGraph('pak_cities.csv')

# Main application
def main():
    # Title and description
    st.title("🗺️ Pakistan Route Planner")
    st.markdown("""
    This application finds the **shortest route** between any two cities in Pakistan 
    using **Dijkstra's Algorithm**. 
    
    Select a source and destination city to calculate the optimal path!
    """)
    
    # Load the graph
    try:
        graph = load_graph()
        cities = graph.get_city_names()
        
        st.success(f"✅ Loaded {len(cities)} Pakistani cities")
        
    except FileNotFoundError:
        st.error("❌ Error: pak_cities.csv not found. Please run data_preparation.py first.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()
    
    # Create two columns for source and destination selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏁 Source City")
        source_city = st.selectbox(
            "Select starting city:",
            options=cities,
            key="source"
        )
    
    with col2:
        st.subheader("🎯 Destination City")
        destination_city = st.selectbox(
            "Select ending city:",
            options=cities,
            key="destination"
        )
    
    # Add some spacing
    st.markdown("---")
    
    # Calculate button
    if st.button("🚀 Calculate Shortest Route", type="primary", use_container_width=True):
        
        # Validation
        if source_city == destination_city:
            st.warning("⚠️ Source and destination cities are the same!")
            return
        
        # Show spinner while calculating
        with st.spinner("Calculating shortest path..."):
            path, distance = graph.dijkstra(source_city, destination_city)
        
        # Display results
        if path and distance:
            st.success("✅ Shortest route found!")
            
            # Display the path
            st.markdown("### 🛣️ Route")
            st.markdown(f"**{' → '.join(path)}**")
            
            # Display total distance
            st.markdown("### 📏 Total Distance")
            st.metric(label="Distance", value=f"{distance:.2f} km")
            
            # Create two columns for tabular and graphical presentation
            col_a, col_b = st.columns([1, 1.5])
            
            with col_a:
                st.markdown("### 📊 Cities in Path (Tabular)")
                
                # Get city coordinates for the path
                route_data = []
                cumulative_distance = 0
                
                for i, city in enumerate(path):
                    coords = graph.cities[city]
                    
                    # Calculate distance from previous city
                    if i > 0:
                        prev_city = path[i-1]
                        prev_coords = graph.cities[prev_city]
                        from dijkstra_algorithm import calculate_distance_km
                        segment_distance = calculate_distance_km(
                            prev_coords['lat'], prev_coords['lon'],
                            coords['lat'], coords['lon']
                        )
                        cumulative_distance += segment_distance
                        distance_str = f"{segment_distance:.2f} km"
                        cumulative_str = f"{cumulative_distance:.2f} km"
                    else:
                        distance_str = "Start"
                        cumulative_str = "0.00 km"
                    
                    route_data.append({
                        "Step": i + 1,
                        "City": city,
                        "Latitude": f"{coords['lat']:.4f}",
                        "Longitude": f"{coords['lon']:.4f}",
                        "Distance from Prev": distance_str,
                        "Total Distance": cumulative_str
                    })
                
                df_route = pd.DataFrame(route_data)
                st.dataframe(df_route, use_container_width=True, hide_index=True)
                
                # Show summary
                st.info(f"**Total cities in route: {len(path)}** | **Total distance: {distance:.2f} km**")
            
            with col_b:
                st.markdown("### 🗺️ Route Visualization (Graphical)")
                
                # Create map visualization
                fig = go.Figure()
                
                # Extract coordinates for the shortest path
                lats = [graph.cities[city]['lat'] for city in path]
                lons = [graph.cities[city]['lon'] for city in path]
                
                # Draw the shortest path as a green line on top
                fig.add_trace(go.Scattergeo(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    line=dict(width=3, color='green'),
                    name='Shortest Path',
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Show all intermediate cities with markers and labels
                for idx, city in enumerate(path):
                    is_start = (idx == 0)
                    is_end = (idx == len(path) - 1)
                    
                    if is_start:
                        # Start city - Blue circle
                        fig.add_trace(go.Scattergeo(
                            lon=[lons[idx]],
                            lat=[lats[idx]],
                            mode='markers+text',
                            marker=dict(size=15, color='blue', symbol='circle'),
                            text=[f'{city}'],
                            textposition='top center',
                            textfont=dict(size=10, color='blue', family='Arial Black'),
                            name='Start',
                            showlegend=False,
                            hovertemplate=f'<b>START: {city}</b><br>Lat: {lats[idx]:.4f}<br>Lon: {lons[idx]:.4f}<extra></extra>'
                        ))
                    elif is_end:
                        # End city - Orange square
                        fig.add_trace(go.Scattergeo(
                            lon=[lons[idx]],
                            lat=[lats[idx]],
                            mode='markers+text',
                            marker=dict(size=15, color='orange', symbol='square'),
                            text=[f'{city}'],
                            textposition='top center',
                            textfont=dict(size=10, color='orange', family='Arial Black'),
                            name='End',
                            showlegend=False,
                            hovertemplate=f'<b>END: {city}</b><br>Lat: {lats[idx]:.4f}<br>Lon: {lons[idx]:.4f}<extra></extra>'
                        ))
                    else:
                        # Intermediate cities - Green diamonds with labels
                        fig.add_trace(go.Scattergeo(
                            lon=[lons[idx]],
                            lat=[lats[idx]],
                            mode='markers+text',
                            marker=dict(size=12, color='green', symbol='diamond'),
                            text=[f'{city}'],
                            textposition='top center',
                            textfont=dict(size=9, color='green'),
                            name='Via',
                            showlegend=False,
                            hovertemplate=f'<b>Via: {city}</b><br>Step {idx+1}<br>Lat: {lats[idx]:.4f}<br>Lon: {lons[idx]:.4f}<extra></extra>'
                        ))
                
                # Update layout for Pakistan region
                fig.update_geos(
                    scope='asia',
                    center=dict(lat=30.0, lon=70.0),
                    projection_scale=8,
                    showcountries=True,
                    countrycolor='lightgray',
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    coastlinecolor='rgb(204, 204, 204)',
                )
                
                fig.update_layout(
                    height=500,
                    margin={"r":0,"t":0,"l":0,"b":0},
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error("❌ No path found between the selected cities!")
    
    # Add footer with information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        <p>Built with Dijkstra's Algorithm | Data from SimpleMaps World Cities Database</p>
        <p>This tool calculates distances using the Haversine formula (great-circle distance)</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
