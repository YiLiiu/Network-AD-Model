import matplotlib.pyplot as plt
import matplotlib.cm as cm

from .models import Network

def plot(network: Network):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    layers = {'OS': 0, 'APP1': 1, 'APP2': 2}

    cmap_os = cm.get_cmap('Blues')
    cmap_app1 = cm.get_cmap('Reds')
    cmap_app2 = cm.get_cmap('Greens')
    num_types = network.num_app_versions  # 假设implementation_type的数量


    for computer in network.computers:
        # determine the color based on the implementation type
        os_color = cmap_os(computer.os.implementation.implementation_type / num_types)
        os_position = (computer.x_position, computer.y_position, layers['OS'])
        ax.scatter(*os_position[:-1], os_position[2], c=os_color, marker='o')
        ax.text(*os_position, f'{computer.id}-OS', color='black')
        
        # store the positions of the apps
        app_positions = []
        
        # APPs
        for app in computer.apps:
            z_layer = layers[app.get_software_type()]
            app_position = (computer.x_position, computer.y_position, z_layer)
            if app.get_software_type() == 'APP1':
                app_color = cmap_app1(app.implementation.implementation_type / num_types)
            elif app.get_software_type() == 'APP2':
                app_color = cmap_app2(app.implementation.implementation_type / num_types)
            ax.scatter(*app_position[:-1], app_position[2], c=app_color, marker='^')
            ax.text(*app_position, f'{computer.id}-{app.get_software_type()}', color='black')
            
            app_positions.append(app_position)
        
        # Draw the edges between OS and APPs
        for app_pos in app_positions:
            ax.plot([os_position[0], app_pos[0]], [os_position[1], app_pos[1]], [os_position[2], app_pos[2]], c='black')

    # Draw the edges
    for app_name, graph in network.graph.items():
        z_layer = layers[app_name]
        for edge in graph.edges():
            x_positions = [network.computers[edge[0].id].x_position, network.computers[edge[1].id].x_position]
            y_positions = [network.computers[edge[0].id].y_position, network.computers[edge[1].id].y_position]
            z_positions = [z_layer, z_layer]
            ax.plot(x_positions, y_positions, z_positions, c='black')
    
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Layer')
    plt.show()