# test
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create random data with numpy
import numpy as np
import random


# TODO : Put the correct joint in the article.
# TODO : Add a curve directly from the app running
# TODO : be able to switch from format artcile et format 16/9 (écran)
# TODO : Change the data shape in the end for export
# TODO : Corrolaire : change the data shape at the beginnning ()

# Question à aborder sur la forme des données.

def create_random_data(
    name_article, name_joint, name_dof, angle_or_translation, name_movement, nb_frame, initialize=False
):
    if initialize:
        df = pd.DataFrame(
            {
                "article": [],# Article name should be the comination of the article and the subejct name (id_subject)
                "joint": [],
                "angle_translation": [],
                "degree_of_freedom": [],
                "movement": [],
                "humerothoracic_angle": [],
                "value": [],
            }
        )
    else:
        random_x = np.linspace(0, 120, nb_frame)
        random_y0 = np.random.randn(nb_frame) + 5
        df = pd.DataFrame(
            {
                "article": [name_article] * nb_frame,
                "joint": [name_joint] * nb_frame,
                "angle_translation": [angle_or_translation] * nb_frame,
                "degree_of_freedom": [name_dof] * nb_frame,
                "movement": [name_movement] * nb_frame,
                "humerothoracic_angle": random_x,
                "value": random_y0,
            }
        )

    return df


def Generation_Full_Article(nb_article):
    nb_joint_by_article = [1, 2, 3]
    nb_dof_by_joint_angle = [0, 1, 2, 3]
    nb_dof_by_joint_translation = [0, 1, 2, 3]
    nb_movement_by_article = [1, 2, 3, 4]

    name_joints = ["Humerothoracic", "Acromioclavicular", "Glenohumeral", "Scapulothoracic"]
    name_movements = ["Movement_1", "Movement_2", "Movement_3", "Movement_4"]
    dof_translation = ["X", "Y", "Z"]
    dof_angle = ["Flexion", "Abduction", "External_rotation"]
    nb_frame = [6, 20, 30]
    df = create_random_data("", "", "", "", "", 6, initialize=True)
    for i in range(nb_article):
        name_article = "Article_" + str(i)
        final_nb_frame = random.choice(nb_frame)
        final_nb_joint = random.choice(nb_joint_by_article)
        final_list_joint = random.sample(name_joints, final_nb_joint)

        final_number_dof_angle = random.choice(nb_dof_by_joint_angle)
        final_dof_angle = random.sample(dof_angle, final_number_dof_angle)

        final_number_dof_translation = random.choice(nb_dof_by_joint_translation)
        final_dof_angle_translation = random.sample(dof_translation, final_number_dof_translation)

        final_number_movement = random.choice(nb_movement_by_article)
        final_list_movement = random.sample(name_movements, final_number_movement)

        for name_joint in final_list_joint:
            for name_movement in final_list_movement:
                for name_dof in final_dof_angle:
                    df_temp = create_random_data(
                        name_article, name_joint, name_dof, "Angle", name_movement, final_nb_frame
                    )
                    df = pd.concat([df, df_temp])
                for name_dof in final_dof_angle_translation:
                    df_temp = create_random_data(
                        name_article, name_joint, name_dof, "Translation", name_movement, final_nb_frame
                    )
                    df = pd.concat([df, df_temp])

    return df

toto = Generation_Full_Article(30)


app = Dash(__name__)

app.layout = html.Div(
    [   # Global Title of the graph
        html.H4("Kinematics of the shoulder joint"),
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
        # Plot the graph
        dcc.Graph(id="graph"),
        # Show the different options in different collumn
        dcc.Dropdown(
            id="movement",
            options=sorted([i for i in toto.movement.unique()]),
            value=sorted([i for i in toto.movement.unique()])[0],
        ),
        dcc.Checklist(
            id="joint",
            options=sorted([i for i in toto.joint.unique()]),
            value=sorted([i for i in toto.joint.unique()]),
            inline=True,
        ),
        dcc.Dropdown(
            options=sorted([i for i in toto.angle_translation.unique()]),
            value=sorted([i for i in toto.angle_translation.unique()])[0],
            id="angle_translation",
        ),
    ])



@app.callback(
Output("download-dataframe-csv", "data"),
    Input("movement", "value"),
    Input("joint", "value"),
    Input("angle_translation", "value"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call = True,)

def export_data(movement,joint,angle_translation,n_clicks):
    df = toto  # replace with your own data source
    mask_joint = df.joint.isin(joint)
    mask_mvt = df.movement.isin([movement])
    # We have to put Angle translation in a list because it is a string
    mask_angle_translation = df.angle_translation.isin([angle_translation])
    # In order to have the data in the correct orger we have to define a list ordering the data
    list_joint_graph_base_in_order = ["Humerothoracic", "Glenohumeral", "Scapulothoracic", "Acromioclavicular"]
    # Adapt the list to the number of degree of freedom selectionned by the user.
    list_to_plot_in_order = []
    for name_joint in list_joint_graph_base_in_order:
        if name_joint in joint:
            list_to_plot_in_order.append(name_joint)

    data_to_export = df[mask_mvt & mask_joint & mask_angle_translation]
    return dcc.send_data_frame(data_to_export.to_csv, "mydf.csv")

@app.callback(
    Output("graph", "figure"),
    Input("movement", "value"),
    Input("joint", "value"),
    Input("angle_translation", "value"),
)
def update_line_chart(movement, joint, angle_translation):
    df = toto  # replace with your own data source
    mask_joint = df.joint.isin(joint)
    mask_mvt = df.movement.isin([movement])
    # We have to put Angle translation in a list because it is a string
    mask_angle_translation = df.angle_translation.isin([angle_translation])
    # In order to have the data in the correct orger we have to define a list ordering the data
    list_joint_graph_base_in_order = ["Humerothoracic", "Glenohumeral", "Scapulothoracic", "Acromioclavicular"]
    # Adapt the list to the number of degree of freedom selectionned by the user.
    list_to_plot_in_order = []
    for name_joint in list_joint_graph_base_in_order:
        if name_joint in joint:
            list_to_plot_in_order.append(name_joint)

    if angle_translation == "Angle":
        list_orga = ["Flexion", "Abduction", "External_rotation"]
    elif angle_translation == "Translation":
        list_orga = ["X", "Y", "Z"]
    fig = px.line(
        df[mask_mvt & mask_joint & mask_angle_translation],
        x="humerothoracic_angle",
        y="value",
        color="article",
        facet_row="joint",
        facet_col="degree_of_freedom",
        category_orders={"degree_of_freedom": list_orga, "joint": list_to_plot_in_order},
    )
    # Allow to remove the "Mvt=" in the legend
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    # here to switch between different layout

    fig.update_layout(
        # If we fix only the height the width will be adapted to the size of the screen
        # However not fixing the height AND the width make the graph not readable
        height=800,
        #width=1500,
        paper_bgcolor="rgba(255,255,255,1)",
        plot_bgcolor="rgba(255,255,255,1)",
        legend=dict(
            title_font_family="Times New Roman",
            font=dict(family="Times New Roman", color="black", size=16),
            orientation="v",
            x=1,
            y=1,
        ),
        font=dict(
            size=16,
            family="Times New Roman",
        ),
        yaxis=dict(color="black"),
        template="simple_white",
        boxgap=0.5,
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
