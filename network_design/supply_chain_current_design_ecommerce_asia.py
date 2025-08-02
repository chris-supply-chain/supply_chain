import folium
import pandas as pd
import numpy as np
from folium import plugins
import json

def create_supply_chain_map():
    """
    Create an interactive supply chain current design map using folium
    """
    
    # Define supply chain facilities for Asian E-commerce Company
    facilities = {
        # Suppliers (Shenzhen area and local)
        'Supplier 1': {'lat': 22.3193, 'lng': 114.1694, 'type': 'supplier', 'capacity': 'High'},
        'Supplier 2': {'lat': 22.5, 'lng': 114.0, 'type': 'supplier', 'capacity': 'High'},
        'Supplier 3': {'lat': 22.2, 'lng': 114.3, 'type': 'supplier', 'capacity': 'High'},
        'Supplier 4': {'lat': 22.4, 'lng': 114.1, 'type': 'supplier', 'capacity': 'Medium'},
        'Supplier 5': {'lat': 22.3, 'lng': 114.2, 'type': 'supplier', 'capacity': 'Medium'},
        'Supplier 6': {'lat': 25.0330, 'lng': 121.5654, 'type': 'supplier', 'capacity': 'Medium'},
        'Supplier 7': {'lat': 24.1477, 'lng': 120.6736, 'type': 'supplier', 'capacity': 'Medium'},
        'Supplier 8': {'lat': 22.6273, 'lng': 120.3014, 'type': 'supplier', 'capacity': 'Medium'},
        'Supplier 9': {'lat': 23.5, 'lng': 121.0, 'type': 'supplier', 'capacity': 'Medium'},
        'Supplier 10': {'lat': 24.8, 'lng': 120.9, 'type': 'supplier', 'capacity': 'Medium'},
        
        # Main Distribution Centers (High Capacity)
        'Main DC 1': {'lat': 25.0330, 'lng': 121.5654, 'type': 'main_dc', 'capacity': 'High'},
        'Main DC 2': {'lat': 24.1477, 'lng': 120.6736, 'type': 'main_dc', 'capacity': 'High'},
        'Main DC 3': {'lat': 35.6762, 'lng': 139.6503, 'type': 'main_dc', 'capacity': 'High'},
        
        # Regional Distribution Centers
        'Regional DC 1': {'lat': 22.6273, 'lng': 120.3014, 'type': 'regional_dc', 'capacity': 'Medium'},
        'Regional DC 2': {'lat': 23.5, 'lng': 121.0, 'type': 'regional_dc', 'capacity': 'Medium'},
        'Regional DC 3': {'lat': 24.8, 'lng': 120.9, 'type': 'regional_dc', 'capacity': 'Medium'},
        'Regional DC 4': {'lat': 22.9, 'lng': 120.6, 'type': 'regional_dc', 'capacity': 'Medium'},
        'Regional DC 5': {'lat': 34.7, 'lng': 135.5, 'type': 'regional_dc', 'capacity': 'Medium'},
        'Regional DC 6': {'lat': 35.4, 'lng': 139.6, 'type': 'regional_dc', 'capacity': 'Medium'},
        
        # Taiwan Ports
        'Kaohsiung Port': {'lat': 22.6163, 'lng': 120.3133, 'type': 'port', 'capacity': 'High'},
        'Taipei Port': {'lat': 25.0330, 'lng': 121.5654, 'type': 'port', 'capacity': 'Medium'},
        
        # Japan Ports
        'Tokyo Port': {'lat': 35.6762, 'lng': 139.6503, 'type': 'port', 'capacity': 'High'},
        'Osaka Port': {'lat': 34.6937, 'lng': 135.5023, 'type': 'port', 'capacity': 'Medium'},
        
        # Fulfillment Centers (5 in Taiwan, 4 in Japan)
        'FC 1': {'lat': 25.0330, 'lng': 121.5654, 'type': 'fulfillment', 'capacity': 'High'},
        'FC 2': {'lat': 24.1477, 'lng': 120.6736, 'type': 'fulfillment', 'capacity': 'High'},
        'FC 3': {'lat': 22.6273, 'lng': 120.3014, 'type': 'fulfillment', 'capacity': 'Medium'},
        'FC 4': {'lat': 23.5, 'lng': 121.0, 'type': 'fulfillment', 'capacity': 'Medium'},
        'FC 5': {'lat': 24.8, 'lng': 120.9, 'type': 'fulfillment', 'capacity': 'Medium'},
        'FC 6': {'lat': 35.8, 'lng': 139.7, 'type': 'fulfillment', 'capacity': 'High'},
        'FC 7': {'lat': 34.8, 'lng': 135.6, 'type': 'fulfillment', 'capacity': 'Medium'},
        'FC 8': {'lat': 35.5, 'lng': 139.8, 'type': 'fulfillment', 'capacity': 'Medium'},
        'FC 9': {'lat': 35.9, 'lng': 140.7, 'type': 'fulfillment', 'capacity': 'Medium'}
    }
    
    # Define supply chain routes for Asian E-commerce Company
    routes = [
        # Suppliers to Main DCs (High Volume)
        {'from': 'Supplier 1', 'to': 'Main DC 1', 'type': 'supplier_to_main', 'volume': 'High'},
        {'from': 'Supplier 2', 'to': 'Main DC 1', 'type': 'supplier_to_main', 'volume': 'High'},
        {'from': 'Supplier 3', 'to': 'Main DC 2', 'type': 'supplier_to_main', 'volume': 'High'},
        {'from': 'Supplier 4', 'to': 'Main DC 2', 'type': 'supplier_to_main', 'volume': 'Medium'},
        {'from': 'Supplier 5', 'to': 'Main DC 1', 'type': 'supplier_to_main', 'volume': 'Medium'},
        {'from': 'Supplier 6', 'to': 'Main DC 3', 'type': 'supplier_to_main', 'volume': 'Medium'},
        {'from': 'Supplier 7', 'to': 'Main DC 1', 'type': 'supplier_to_main', 'volume': 'Medium'},
        {'from': 'Supplier 8', 'to': 'Main DC 2', 'type': 'supplier_to_main', 'volume': 'Medium'},
        {'from': 'Supplier 9', 'to': 'Main DC 1', 'type': 'supplier_to_main', 'volume': 'Medium'},
        {'from': 'Supplier 10', 'to': 'Main DC 1', 'type': 'supplier_to_main', 'volume': 'Medium'},
        
        # Shenzhen Suppliers to Taiwan Ports (Ocean Shipping)
        {'from': 'Supplier 1', 'to': 'Kaohsiung Port', 'type': 'shenzhen_to_port', 'volume': 'High'},
        {'from': 'Supplier 2', 'to': 'Kaohsiung Port', 'type': 'shenzhen_to_port', 'volume': 'High'},
        {'from': 'Supplier 3', 'to': 'Taipei Port', 'type': 'shenzhen_to_port', 'volume': 'Medium'},
        {'from': 'Supplier 4', 'to': 'Kaohsiung Port', 'type': 'shenzhen_to_port', 'volume': 'Medium'},
        {'from': 'Supplier 5', 'to': 'Taipei Port', 'type': 'shenzhen_to_port', 'volume': 'Medium'},
        
        # Shenzhen Suppliers to Japan Ports (Ocean Shipping)
        {'from': 'Supplier 1', 'to': 'Tokyo Port', 'type': 'shenzhen_to_port', 'volume': 'High'},
        {'from': 'Supplier 2', 'to': 'Tokyo Port', 'type': 'shenzhen_to_port', 'volume': 'High'},
        {'from': 'Supplier 3', 'to': 'Osaka Port', 'type': 'shenzhen_to_port', 'volume': 'Medium'},
        {'from': 'Supplier 4', 'to': 'Tokyo Port', 'type': 'shenzhen_to_port', 'volume': 'Medium'},
        {'from': 'Supplier 5', 'to': 'Osaka Port', 'type': 'shenzhen_to_port', 'volume': 'Medium'},
        
        # Taiwan Ports to Regional DCs
        {'from': 'Kaohsiung Port', 'to': 'Regional DC 1', 'type': 'port_to_regional', 'volume': 'High'},
        {'from': 'Kaohsiung Port', 'to': 'Regional DC 2', 'type': 'port_to_regional', 'volume': 'High'},
        {'from': 'Taipei Port', 'to': 'Regional DC 3', 'type': 'port_to_regional', 'volume': 'Medium'},
        {'from': 'Taipei Port', 'to': 'Regional DC 4', 'type': 'port_to_regional', 'volume': 'Medium'},
        
        # Japan Ports to Regional DCs
        {'from': 'Tokyo Port', 'to': 'Regional DC 5', 'type': 'port_to_regional', 'volume': 'High'},
        {'from': 'Tokyo Port', 'to': 'Regional DC 6', 'type': 'port_to_regional', 'volume': 'High'},
        {'from': 'Osaka Port', 'to': 'Regional DC 5', 'type': 'port_to_regional', 'volume': 'Medium'},
        {'from': 'Osaka Port', 'to': 'Regional DC 6', 'type': 'port_to_regional', 'volume': 'Medium'},
        
        # Main DCs to Regional DCs (Cross-docking)
        {'from': 'Main DC 1', 'to': 'Regional DC 1', 'type': 'main_to_regional', 'volume': 'High'},
        {'from': 'Main DC 1', 'to': 'Regional DC 2', 'type': 'main_to_regional', 'volume': 'High'},
        {'from': 'Main DC 2', 'to': 'Regional DC 3', 'type': 'main_to_regional', 'volume': 'High'},
        {'from': 'Main DC 2', 'to': 'Regional DC 4', 'type': 'main_to_regional', 'volume': 'High'},
        {'from': 'Main DC 3', 'to': 'Regional DC 5', 'type': 'main_to_regional', 'volume': 'Medium'},
        
        # Regional DCs to Fulfillment Centers (Taiwan)
        {'from': 'Regional DC 1', 'to': 'FC 1', 'type': 'regional_to_fc', 'volume': 'High'},
        {'from': 'Regional DC 2', 'to': 'FC 2', 'type': 'regional_to_fc', 'volume': 'High'},
        {'from': 'Regional DC 3', 'to': 'FC 3', 'type': 'regional_to_fc', 'volume': 'Medium'},
        {'from': 'Regional DC 4', 'to': 'FC 4', 'type': 'regional_to_fc', 'volume': 'Medium'},
        {'from': 'Regional DC 4', 'to': 'FC 5', 'type': 'regional_to_fc', 'volume': 'Medium'},
        
        # Regional DCs to Fulfillment Centers (Japan)
        {'from': 'Regional DC 5', 'to': 'FC 6', 'type': 'regional_to_fc', 'volume': 'High'},
        {'from': 'Regional DC 5', 'to': 'FC 7', 'type': 'regional_to_fc', 'volume': 'Medium'},
        {'from': 'Regional DC 6', 'to': 'FC 8', 'type': 'regional_to_fc', 'volume': 'Medium'},
        {'from': 'Regional DC 6', 'to': 'FC 9', 'type': 'regional_to_fc', 'volume': 'Medium'},
        
        # Direct Main DC to FC (High Priority)
        {'from': 'Main DC 1', 'to': 'FC 1', 'type': 'main_to_fc', 'volume': 'High'},
        {'from': 'Main DC 2', 'to': 'FC 2', 'type': 'main_to_fc', 'volume': 'High'}
    ]
    
    # Create the base map centered on Asia-Pacific region
    m = folium.Map(
        location=[20.0, 110.0],
        zoom_start=5,
        tiles='OpenStreetMap',
        attributionControl=False
    )
    
    # Define colors for different facility types
    facility_colors = {
        'supplier': 'green',
        'main_dc': 'blue',
        'regional_dc': 'lightblue',
        'port': 'darkblue',
        'fulfillment': 'purple'
    }
    
    # Define colors for different route types (bolder colors)
    route_colors = {
        'supplier_to_main': '#00FF00',      # Bright green
        'supplier_to_regional': '#90EE90',  # Light green
        'shenzhen_to_port': '#008000',      # Dark green
        'port_to_regional': '#0000FF',      # Blue
        'main_to_regional': '#0066FF',      # Bold blue
        'regional_to_fc': '#FF00FF',        # Bright purple
        'main_to_fc': '#FF6600'             # Orange
    }
    
    # Add facility markers
    for facility_name, facility_data in facilities.items():
        color = facility_colors[facility_data['type']]
        
        # Create popup content
        popup_content = f"""
        <div style="width: 200px;">
            <h4>{facility_name}</h4>
            <p><strong>Type:</strong> {facility_data['type'].title()}</p>
            <p><strong>Capacity:</strong> {facility_data['capacity']}</p>
            <p><strong>Coordinates:</strong> {facility_data['lat']:.4f}, {facility_data['lng']:.4f}</p>
        </div>
        """
        
        # Add marker with different icons based on facility type
        if facility_data['type'] == 'supplier':
            icon = folium.Icon(color=color, icon='leaf', prefix='fa')
        elif facility_data['type'] == 'main_dc':
            icon = folium.Icon(color=color, icon='warehouse', prefix='fa')
        elif facility_data['type'] == 'regional_dc':
            icon = folium.Icon(color=color, icon='truck', prefix='fa')
        elif facility_data['type'] == 'port':
            icon = folium.Icon(color=color, icon='ship', prefix='fa')
        elif facility_data['type'] == 'fulfillment':
            icon = folium.Icon(color=color, icon='box', prefix='fa')
        else:
            icon = folium.Icon(color=color, icon='map-marker', prefix='fa')
        
        folium.Marker(
            location=[facility_data['lat'], facility_data['lng']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=facility_name,
            icon=icon
        ).add_to(m)
    
    # Add route lines with directional arrows
    for route in routes:
        from_facility = facilities[route['from']]
        to_facility = facilities[route['to']]
        
        # Determine line weight based on volume
        weight_map = {'High': 5, 'Medium': 3, 'Low': 1}
        weight = weight_map[route['volume']]
        
        # Determine color based on route type
        color = route_colors[route['type']]
        
        # Create popup content for route
        route_popup = f"""
        <div style="width: 200px;">
            <h4>{route['from']} → {route['to']}</h4>
            <p><strong>Type:</strong> {route['type'].replace('_', ' ').title()}</p>
            <p><strong>Volume:</strong> {route['volume']}</p>
        </div>
        """
        
        # Calculate direction angle based on how the line appears on the map
        import math
        
        # Calculate angle based on how Folium draws straight lines on Web Mercator projection
        # Folium draws straight lines, not geodesic curves
        delta_lat = to_facility['lat'] - from_facility['lat']
        delta_lng = to_facility['lng'] - from_facility['lng']
        
        # For Web Mercator projection, we need to account for longitude compression
        # The angle should match how the line appears on the projected map
        lat_avg = (from_facility['lat'] + to_facility['lat']) / 2
        cos_lat = math.cos(math.radians(lat_avg))
        
        # Adjust longitude for projection (this is how Folium sees it)
        delta_lng_adjusted = delta_lng * cos_lat
        
        # Calculate angle in the projected space
        angle = math.degrees(math.atan2(delta_lat, delta_lng_adjusted))
        

        
        # Calculate three points along the route using distance-based positioning
        # This mirrors how Folium calculates positions along PolyLines
        import math
        
        # Calculate total distance (simplified for straight lines)
        total_distance = math.sqrt((to_facility['lat'] - from_facility['lat'])**2 + 
                                  (to_facility['lng'] - from_facility['lng'])**2)
        
        # Position arrows at 30%, 50%, and 70% of the actual distance
        distances = [0.3, 0.5, 0.7]
        arrow_positions = []
        
        for dist_ratio in distances:
            # Calculate position based on distance ratio
            arrow_lat = from_facility['lat'] + (to_facility['lat'] - from_facility['lat']) * dist_ratio
            arrow_lng = from_facility['lng'] + (to_facility['lng'] - from_facility['lng']) * dist_ratio
            arrow_positions.append((arrow_lat, arrow_lng))
        
        # Draw the route line
        folium.PolyLine(
            locations=[[from_facility['lat'], from_facility['lng']], 
                      [to_facility['lat'], to_facility['lng']]],
            popup=folium.Popup(route_popup, max_width=300),
            color=color,
            weight=weight,
            opacity=0.7
        ).add_to(m)
        
        # Create SVG arrow that follows the line direction
        arrow_size = weight * 4.8  # Reduced by 20% (6 * 0.8 = 4.8)
        arrow_html = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 {arrow_size} {arrow_size}">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                        refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="{color}" />
                </marker>
            </defs>
            <line x1="0" y1="{arrow_size//2}" x2="{arrow_size}" y2="{arrow_size//2}" 
                  stroke="{color}" stroke-width="3" marker-end="url(#arrowhead)" />
        </svg>
        """
        
        # Add three directional arrows along the route
        for i, (arrow_lat, arrow_lng) in enumerate(arrow_positions):
            folium.Marker(
                location=[arrow_lat, arrow_lng],
                popup=folium.Popup(route_popup, max_width=300),
                tooltip=f"{route['from']} → {route['to']} (Arrow {i+1})",
                icon=folium.DivIcon(
                    html=arrow_html,
                    icon_size=(arrow_size, arrow_size),
                    icon_anchor=(arrow_size//2, arrow_size//2)
                )
            ).add_to(m)
    
    # Add a legend
    legend_html = '''
    <div style="position: fixed; 
                top: 50px; left: 50px; width: 250px; height: 350px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <h4>E-commerce Network Legend</h4>
    <p><i class="fa fa-leaf" style="color:green"></i> Suppliers (10)</p>
    <p><i class="fa fa-warehouse" style="color:blue"></i> Main DCs (3)</p>
    <p><i class="fa fa-ship" style="color:darkblue"></i> Ports (4)</p>
    <p><i class="fa fa-truck" style="color:lightblue"></i> Regional DCs (6)</p>
    <p><i class="fa fa-box" style="color:purple"></i> Fulfillment Centers (9)</p>
    <p><span style="color:green">━━━</span> Supplier to Main DC</p>
    <p><span style="color:darkgreen">━━━</span> Supplier to Port</p>
    <p><span style="color:blue">━━━</span> Port to Regional DC</p>
    <p><span style="color:lightblue">━━━</span> Main to Regional DC</p>
    <p><span style="color:purple">━━━</span> Regional DC to FC</p>
    <p><span style="color:orange">━━━</span> Main DC to FC (Direct)</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add fullscreen option
    plugins.Fullscreen().add_to(m)
    
    return m

def add_supply_chain_metrics(map_obj):
    """
    Add supply chain performance metrics to the map
    """
    # Create a metrics panel
    metrics_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 300px; height: 400px; 
                background-color: rgba(255,255,255,0.95); border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; backdrop-filter: blur(5px);">
    <h4>E-commerce Network Summary</h4>
    <p><strong>Network Structure:</strong></p>
    <p>• Suppliers: 10</p>
    <p>• Main DCs: 3</p>
    <p>• Ports: 4</p>
    <p>• Regional DCs: 6</p>
    <p>• Fulfillment Centers: 9</p>
    <p>• Total Routes: 35</p>
    <p><strong>Cost Breakdown (Annual):</strong></p>
    <p>• Shipping Cost: $12.5M</p>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;• Ocean Cost: $8.2M</p>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;• Inland FTL Cost: $4.3M</p>
    <p>• Fixed Cost: $8.2M</p>
    <p>• Variable Cost: $15.3M</p>
    <p><strong>Total Network Cost: $36.0M</strong></p>
    </div>
    '''
    map_obj.get_root().html.add_child(folium.Element(metrics_html))

def main():
    """
    Main function to create and save the supply chain map
    """
    print("Creating supply chain current design map...")
    
    # Create the map
    supply_chain_map = create_supply_chain_map()
    
    # Add metrics panel
    add_supply_chain_metrics(supply_chain_map)
    
    # Save the map
    output_file = 'supply_chain_current_design_asian_ecommerce.html'
    supply_chain_map.save(output_file)
    
    print(f"Asian e-commerce supply chain map created successfully!")
    print(f"Map saved as: {output_file}")
    print(f"Open {output_file} in your web browser to view the interactive map.")
    
    return supply_chain_map

if __name__ == "__main__":
    # Create the map
    map_obj = main()
    
    # Display additional information
    print("\n" + "="*50)
    print("ASIAN E-COMMERCE SUPPLY CHAIN CURRENT DESIGN")
    print("="*50)
    print("This map shows:")
    print("• Manufacturing plants (red markers)")
    print("• Distribution centers (blue markers)")
    print("• Fulfillment centers (purple markers)")
    print("• Suppliers (green markers)")
    print("• Retail stores (orange markers)")
    print("• Supply chain routes with different colors and thicknesses")
    print("• Interactive popups with facility and route information")
    print("• Legend and metrics panel")
    print("• Fullscreen and minimap features")
    print("="*50) 