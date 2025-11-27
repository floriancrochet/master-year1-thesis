# Standard libraries
import math

# Data manipulation
import pandas as pd

# Dash core components
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from dash.dash_table.Format import Format, Scheme, Sign

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Plotly for visualization
import plotly.express as px
import plotly.graph_objects as go


# =================================================================================
#                        Initialisation de l'application
# =================================================================================

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
    ],
)
server = app.server


# =================================================================================
#                             Fonctions utiles
# =================================================================================


def format_decimal(x):
    return f"{x:,.2f}".replace(",", " ").replace(".", ",")


def format_entier(x):
    return f"{x:,}".replace(",", " ").replace(".", ",")


def format_scientifique(x):
    try:
        return f"{x:.2e}"
    except:
        return x


# =================================================================================
#                             Listes utiles
# =================================================================================

# =========================================
#                modèles
# =========================================

modeles = [
    "Ridge",
    "Lasso",
    "Elastic Net (α = 0.5)",
    "Elastic Net",
    "Adaptive Lasso",
    "Ridge (DC-SIS)",
    "Lasso (DC-SIS)",
    "Elastic Net (DC-SIS) (α = 0.5)",
    "Elastic Net (DC-SIS)",
    "Adaptive Lasso (DC-SIS)",
]

couleurs_modeles = {
    "Ridge": "#1f77b4",  # bleu classique
    "Lasso": "#ff7f0e",  # orange
    "Elastic Net (α = 0.5)": "#2ca02c",  # vert
    "Elastic Net": "#d62728",  # rouge brique
    "Adaptive Lasso": "#9467bd",  # violet
    "Ridge (DC-SIS)": "#8c564b",  # brun
    "Lasso (DC-SIS)": "#e377c2",  # rose
    "Elastic Net (DC-SIS) (α = 0.5)": "#7f7f7f",  # gris
    "Elastic Net (DC-SIS)": "#bcbd22",  # jaune olive
    "Adaptive Lasso (DC-SIS)": "#17becf",  # bleu turquoise
}


# =================================================================================
#                             Contenu de l'application
# =================================================================================

# =========================================
#               En-tête amélioré
# =========================================

options_modeles = [{"label": "Tous les modèles", "value": "all"}] + [
    {"label": m, "value": m} for m in sorted(set(modeles))
]

entete_appli = html.Div(
    [
        # Logo
        html.Img(
            src="/assets/sp500.png",
            style={
                "height": "15vh",
                "marginLeft": "0.2vw",
                "marginRight": "1vw",
                "borderRadius": "0.5vw",
            },
        ),
        # Titre
        html.H1(
            [
                html.Span(
                    "Tableau de bord", style={"color": "white", "display": "block"}
                ),
                html.Span(
                    "des performances", style={"color": "#FFD700", "display": "block"}
                ),
            ],
            style={
                "fontSize": "7vh",
                "fontWeight": "bold",
                "lineHeight": "1.1",
                "margin": "0 14.5vw 0 0",
                "alignItems": "center",
            },
        ),
        # Dropdown
        dcc.Dropdown(
            id="filtre-modeles",
            options=options_modeles,
            multi=True,
            value=None,
            placeholder="Sélectionnez un ou plusieurs modèles",
            persistence=True,
            persistence_type="memory",
            style={
                "width": "26.5vw",
                "height": "5.5vh",
                "font-size": "2.2vh",
                "color": "black",
                "margin": "0",
                "position": "relative",
                "zIndex": 10000,
            },
        ),
        # Bouton reset
        dbc.Button(
            html.I(className="bi-arrow-clockwise"),
            id="reset-filters",
            color="light",
            style={
                "fontSize": "3.5vh",
                "fontWeight": "bold",
                "padding": "0vh 0.8vh",
                "marginLeft": "0.5vw",
                # "backgroundColor": "#395C93",
            },
        ),
    ],
    style={
        "height": "17vh",
        "display": "flex",
        "alignItems": "center",
    },
)


# =========================================
#                Légende
# =========================================

# -----------------------------------------
# Fonction
# -----------------------------------------


def construire_legende_modeles(modeles_affiches):
    legend_items = []
    for modele in modeles_affiches:
        if modele not in couleurs_modeles:
            continue
        item = html.Div(
            [
                html.Span(
                    style={
                        "display": "inline-block",
                        "width": "2vw",
                        "height": "2vw",
                        "backgroundColor": couleurs_modeles[modele],
                        "marginRight": "0.5vw",
                        "border": "0.1vw solid black",
                        "borderRadius": "0.5vw",
                    }
                ),
                html.Span(
                    modele,
                    style={
                        "fontSize": "2.5vh",
                        "color": "black",
                        "fontWeight": "bold",
                        "whiteSpace": "nowrap",
                    },
                ),
            ],
            style={"display": "flex", "alignItems": "center", "margin": "1vh 0.5vw"},
        )
        legend_items.append(item)

    return html.Div(
        legend_items,
        style={
            "display": "grid",
            "justifyItems": "start",
            "gridTemplateColumns": f"repeat({min(len(legend_items), 5)}, 1fr)",
            "gap": "1.1vh 1.1vw",
            "padding": "1vh",
        },
    )


# -----------------------------------------
# Intégration à l'application
# -----------------------------------------

appli_legende_modeles = html.Div(
    id="legende-modeles",
    children=construire_legende_modeles(modeles),
    style={
        "minWidth": "96.75vw",
        "width": "96.75vw",
        "maxWidth": "96.75vw",
        "display": "grid",
        "justifyItems": "start",
        "borderRadius": "1.5vw",
        "backgroundColor": "#e0e0e0",
        "border": "0.4vw solid #001F3F",
        "padding": "2vh",
        "margin": "2vh auto",
        "gridTemplateColumns": "repeat(5, 1fr)",
        "gap": "1.1vh 1.1vw",
        "boxShadow": "0 0.4vh 0.8vh rgba(0, 0, 0, 0.1)",
        "transition": "all 0.3s ease-in-out",  # pour un effet fluide
    },
)


# =========================================
#             hyperparametres
# =========================================

# -----------------------------------------
# Chargement des données
# -----------------------------------------

hyperparametres = pd.read_csv("data/hyperparameters.csv")

hyperparametres_modeles = {
    "ridge": "Ridge",
    "lasso": "Lasso",
    "en1": "Elastic Net (α = 0.5)",
    "en2": "Elastic Net",
    "adlasso": "Adaptive Lasso",
    "ridge_dcsis": "Ridge (DC-SIS)",
    "lasso_dcsis": "Lasso (DC-SIS)",
    "en1_dcsis": "Elastic Net (DC-SIS) (α = 0.5)",
    "en2_dcsis": "Elastic Net (DC-SIS)",
    "adlasso_dcsis": "Adaptive Lasso (DC-SIS)",
}

hyperparametres["Model"] = hyperparametres["Model"].map(hyperparametres_modeles)
hyperparametres.rename(columns={"Model": "Modele"}, inplace=True)


# -----------------------------------------
# Fonction
# -----------------------------------------

# Diagramme en barres pour les hyperparamètres


def diagramme_hyperparametres(data, y_column, y_label, title, y_range=None):
    # définir le format différent pour lambda
    if y_column == "lambda":
        texte_format = data[y_column].map(lambda x: f"{x:.2e}")
        hovertemplate = f"<b>%{{y}}</b><br>{y_label} = %{{x:.2e}}<extra></extra>"
    else:
        texte_format = data[y_column].map(lambda x: f"{x:.2f}")
        hovertemplate = f"<b>%{{y}}</b><br>{y_label} = %{{x:.2f}}<extra></extra>"

    fig = px.bar(
        data_frame=data,
        x=y_column,
        y="Modele",
        color="Modele",
        labels={y_column: y_label},
        color_discrete_map=couleurs_modeles,
        orientation="h",
        text=texte_format,
    )

    fig.update_traces(
        textposition="outside",
        textfont_size=14,
        cliponaxis=False,
        hovertemplate=hovertemplate,
    )

    if y_range is None:
        x_max = data[y_column].max() * 1.2
    else:
        x_max = y_range[1]

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=21.5, color="black"), x=0.5),
        yaxis=dict(
            showgrid=False,
            automargin=True,
            title="Modèle",
            ticktext=[],
            tickvals=[],
        ),
        xaxis=dict(title=y_label, showgrid=True, range=[0, x_max]),
        showlegend=False,
        margin=dict(t=70, b=50, l=5, r=5),
    )

    return fig


# -----------------------------------------
# Intégration à l'application
# -----------------------------------------

appli_diagramme_alpha = html.Div(
    [
        dcc.Graph(
            id="diag-alpha",
            style={
                "width": "96%",
                "height": "96%",
            },
            config={"responsive": True},
        ),
    ],
    style={
        "width": "47.75vw",
        "height": "70vh",
        "display": "flex",
        "justifyContent": "center",
        "borderRadius": "1.5vw",
        "backgroundColor": "white",
        "border": "0.4vw solid #001F3F",
    },
)

appli_diagramme_lambda = html.Div(
    [
        dcc.Graph(
            id="diag-lambda",
            style={
                "width": "96%",
                "height": "96%",
            },
            config={"responsive": True},
        ),
    ],
    style={
        "width": "47.75vw",
        "height": "70vh",
        "display": "flex",
        "justifyContent": "center",
        "borderRadius": "1.5vw",
        "backgroundColor": "white",
        "border": "0.4vw solid #001F3F",
    },
)


# =========================================
#              nb_variables
# =========================================

# -----------------------------------------
# Chargement des données
# -----------------------------------------

nb_variables = pd.read_csv("data/nb_variables.csv")

colonnes = {
    "stock": "Action",
    "ridge": "Ridge",
    "lasso": "Lasso",
    "en1": "Elastic Net (α = 0.5)",
    "en2": "Elastic Net",
    "adlasso": "Adaptive Lasso",
    "ridge_dcsis": "Ridge (DC-SIS)",
    "lasso_dcsis": "Lasso (DC-SIS)",
    "en1_dcsis": "Elastic Net (DC-SIS) (α = 0.5)",
    "en2_dcsis": "Elastic Net (DC-SIS)",
    "adlasso_dcsis": "Adaptive Lasso (DC-SIS)",
}

nb_variables.rename(columns=colonnes, inplace=True)


# -----------------------------------------
# Fonction
# -----------------------------------------


def diagramme_nb_variables(data):
    data_melt = data.melt(var_name="Modele", value_name="Nb_variables")

    fig = px.bar(
        data_frame=data_melt,
        x="Modele",
        y="Nb_variables",
        color="Modele",
        text="Nb_variables",
        labels={"Modele": "", "Nb_variables": "Nombre de variables"},
        color_discrete_map={"Action": "black", **couleurs_modeles},
    )

    fig.update_traces(
        textposition="outside",
        textfont_size=14,
        cliponaxis=False,
    )

    fig.update_layout(
        title=dict(
            text="<b>Nombre de variables par modèle</b>",
            font=dict(size=21.5, color="black"),
            x=0.5,
        ),
        showlegend=False,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            automargin=True,
        ),
        yaxis=dict(
            title="Nombre de variables",
            automargin=True,
        ),
        margin=dict(t=70, b=20, l=60, r=10),
        annotations=[
            dict(
                text="Modèle",  # Titre personnalisé
                x=0.5,
                y=-0.10,  # Position verticale (en fraction de l’axe)
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16),
            )
        ],
    )

    return fig


# -----------------------------------------
# Intégration à l'application
# -----------------------------------------

appli_diagramme_nb_variables = html.Div(
    [
        dcc.Graph(
            id="diag-nb-var",
            style={
                "width": "96%",
                "height": "96%",
            },
            config={"responsive": True},
        ),
    ],
    style={
        "width": "47.75vw",
        "height": "70vh",
        "display": "flex",
        "justifyContent": "center",
        "borderRadius": "1.5vw",
        "backgroundColor": "white",
        "border": "0.4vw solid #001F3F",
    },
)

# =========================================
#              coefficients
# =========================================

# -----------------------------------------
# Chargement des données
# -----------------------------------------

coefficients = pd.read_csv("data/coefficients.csv")

coefficients.rename(columns=colonnes, inplace=True)


# -----------------------------------------
# Fonction
# -----------------------------------------


def table_coefficients(data):

    columns = []
    for col in data.columns:
        if col == "Action":
            columns.append({"name": "Action", "id": col})
        else:
            columns.append({"name": "", "id": col})

    table = dash_table.DataTable(
        id="table-coefficients",
        columns=columns,
        data=data.to_dict("records"),
        page_action="none",  # désactive totalement la pagination
        style_table={
            "height": "65vh",  # fixe la hauteur
            "overflowY": "auto",  # scroll vertical
            "overflowX": "auto",  # scroll horizontal si besoin
            "minWidth": "100%",
        },
        style_cell={
            "textAlign": "center",
            "font_family": "Arial",
            "font_size": "16px",
            "padding": "8px",
            "maxWidth": "200px",
            "whiteSpace": "normal",
        },
        style_data={
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_header={
            "backgroundColor": "#001F3F",
            "fontWeight": "bold",
            "color": "white",
            "fontSize": "18px",
        },
        style_data_conditional=[],
        fixed_rows={"headers": True},
        sort_action="native",
        filter_action="native",
        filter_options={"placeholder_text": "Filtrer..."},
        export_format="csv",
        style_header_conditional=[
            {
                "if": {"column_id": modele},
                "backgroundColor": couleurs_modeles[modele],
                "color": "white",
            }
            for modele in couleurs_modeles
            if modele in data.columns
        ],
    )

    return table


# -----------------------------------------
# Intégration à l'application
# -----------------------------------------

appli_table_coefficients = html.Div(
    [
        # Bouton superposé
        html.Button(
            "Normaliser les coefficients",
            id="toggle-normalisation",
            n_clicks=0,
            style={
                "position": "absolute",
                "top": "1vh",
                "right": "1vw",
                "zIndex": "10",
                "fontSize": "16px",
                # "padding": "0.25vh 0.5vw",
                "backgroundColor": "#f1efef",
                "color": "black",
                "border": "0.35vh solid #4d4d4d",
                # "borderRadius": "0.5vw",
            },
        ),
        dash_table.DataTable(
            id="table-coefficients",
            columns=[],
            data=[],
            page_action="none",
            style_table={
                "height": "65vh",
                "overflowY": "auto",
                "overflowX": "auto",
                "minWidth": "100%",
            },
            style_cell={
                "textAlign": "center",
                "font_family": "Arial",
                "font_size": "16px",
                "padding": "8px",
                "maxWidth": "200px",
                "whiteSpace": "normal",
            },
            style_data={
                "whiteSpace": "normal",
                "height": "auto",
            },
            style_header={
                "backgroundColor": "#001F3F",
                "fontWeight": "bold",
                "color": "white",
                "fontSize": "18px",
            },
            style_data_conditional=[],
            fixed_rows={"headers": True},
            sort_action="native",
            filter_action="native",
            filter_options={"placeholder_text": "Filtrer..."},
            export_format="csv",
        ),
    ],
    style={
        "width": "47.75vw",
        "height": "70vh",
        "overflow": "hidden",
        "borderRadius": "1.5vw",
        "backgroundColor": "white",
        "border": "0.4vw solid #001F3F",
        "padding": "1vh",
        "position": "relative",  # nécessaire pour que le bouton soit positionné relativement à ce bloc
    },
)


# =========================================
#               PERFORMANCE
# =========================================

# -----------------------------------------
# Chargement des données
# -----------------------------------------

performance = pd.read_csv("data/performance.csv")

performance_modeles = {
    "sp500": "S&P 500",
    "ridge": "Ridge",
    "lasso": "Lasso",
    "en1": "Elastic Net (α = 0.5)",
    "en2": "Elastic Net",
    "adlasso": "Adaptive Lasso",
    "ridge_dcsis": "Ridge (DC-SIS)",
    "lasso_dcsis": "Lasso (DC-SIS)",
    "en1_dcsis": "Elastic Net (DC-SIS) (α = 0.5)",
    "en2_dcsis": "Elastic Net (DC-SIS)",
    "adlasso_dcsis": "Adaptive Lasso (DC-SIS)",
}

performance["Index_ETF"] = performance["Index_ETF"].map(performance_modeles)

# -----------------------------------------
# Fonction de visualisation
# -----------------------------------------


def tracer_performance(df, colonne):
    df_modeles = df[df["Index_ETF"] != "S&P 500"].copy()

    # Formater la valeur avec 4 décimales
    df_modeles["val_formatee"] = df_modeles[colonne].map(lambda x: f"{x:.4f}")

    # Titres personnalisés pour les graphiques
    titres_personnalises = {
        "Tracking_Error": "Erreur de suivi",
        "Active_Return": "Rendements excédentaires",
        "Information_Ratio": "Ratio d'information",
        "Correlation_SP500": "Corrélation",
        "Beta": "Bêta",
        "Jensen_Alpha": "Alpha de Jensen",
    }

    titre = titres_personnalises.get(colonne, colonne.replace("_", " "))

    fig = px.line(
        df_modeles,
        x="Index_ETF",
        y=colonne,
        color="Index_ETF",
        markers=True,
        color_discrete_map=couleurs_modeles,
        text="val_formatee",  # Valeur affichée sur les points
    )

    fig.update_traces(
        marker=dict(size=12),
        textposition="top center",
        textfont=dict(size=14),
    )

    fig.update_layout(
        title=dict(
            text=f"<b>{titre}</b>",
            font=dict(size=20, color="black"),
            x=0.5,
        ),
        xaxis=dict(showticklabels=False, title_text=None),
        yaxis_title=titre,
        showlegend=False,
        annotations=[
            dict(
                text="Modèle",
                x=0.5,
                y=-0.15,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16),
            )
        ],
    )

    return fig


def generer_graphiques_performance(df, modeles_selectionnes=None):
    df_modeles = df[df["Index_ETF"] != "S&P 500"]
    if modeles_selectionnes and modeles_selectionnes != ["all"]:
        df_modeles = df_modeles[df_modeles["Index_ETF"].isin(modeles_selectionnes)]

    mesures = [
        "Tracking_Error",
        "Active_Return",
        "Information_Ratio",
        "Correlation_SP500",
        "Beta",
        "Jensen_Alpha",
    ]

    figures = [
        html.Div(
            dcc.Graph(
                figure=tracer_performance(df_modeles, mesure),
                id=f"graph-performance-{mesure}",
                config={"displayModeBar": False},
            ),
            style={
                "backgroundColor": "white",
                "border": "0.4vw solid #001F3F",
                "borderRadius": "1.5vw",
                "padding": "0.5vw",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            },
        )
        for mesure in mesures
    ]

    return figures


# -----------------------------------------
# Intégration à l'application
# -----------------------------------------

# Création des graphiques dans l'ordre
appli_diagramme_performance = html.Div(
    id="bloc-performance",
    style={
        "width": "96.75vw",
        "backgroundColor": "#e0e0e0",
        "borderRadius": "1.5vw",
        "border": "0.4vw solid #001F3F",
        "padding": "0.5vw",
        "display": "flex",
        "flexDirection": "column",
        "gap": "2vh",
    },
)


# =========================================
#             data_performance
# =========================================

# -----------------------------------------
# Chargement des données
# -----------------------------------------

data_performance = pd.read_csv("data/data_performance.csv")
data_performance.rename(
    columns={k: v for k, v in colonnes.items() if k in data_performance.columns},
    inplace=True,
)
data_performance["date"] = pd.to_datetime(
    data_performance["date"]
)  # Convertir la colonne "date" en datetime


# -----------------------------------------
# Fonction
# -----------------------------------------


# -----------------------------------------
# Intégration à l'application
# -----------------------------------------


# ==================================================================================
#                               Interface utilisateur
# ==================================================================================

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [entete_appli],
                    style={
                        "height": "19vh",
                        "display": "flex",
                        "alignItems": "center",
                        "backgroundColor": "#395C93",
                    },
                    md=12,
                ),
            ]
        ),
        # Ajout de la légende
        dbc.Row(
            [
                dbc.Col(
                    [appli_legende_modeles],
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "backgroundColor": "#6E8DBE",
                        "padding": "0",
                    },
                    md=12,
                ),
            ]
        ),
        # Graphiques
        dbc.Row(
            [
                dbc.Col(
                    appli_diagramme_alpha,
                    md=6,
                    style={
                        "padding": "0 0.5vw 1vh 1vw",
                    },
                ),
                dbc.Col(
                    appli_diagramme_lambda,
                    md=6,
                    style={
                        "padding": "0 1vw 1vh 0.5vw",
                    },
                ),
            ],
            style={
                "height": "72vh",
                "backgroundColor": "#6E8DBE",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    appli_diagramme_nb_variables,
                    md=6,
                    style={
                        "padding": "0 0.5vw 1vh 1vw",
                    },
                ),
                dbc.Col(
                    [
                        # STORE doit venir avant les callbacks dépendants
                        dcc.Store(id="etat-normalisation", data=False),
                        appli_table_coefficients,
                    ],
                    md=6,
                    style={
                        "padding": "0 1vw 1vh 0.5vw",
                    },
                ),
            ],
            style={
                "height": "72vh",
                "backgroundColor": "#6E8DBE",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    appli_diagramme_performance,
                    md=12,
                    style={
                        "backgroundColor": "#6E8DBE",
                        "padding": "0 1vw 0vh 1vw",
                    },
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.P(
                        [
                            "Cette application présente les résultats du mémoire intitulé ",
                            html.Em("Index tracking et sélection des actifs"),
                            ", réalisé par Florian CROCHET sous la direction du professeur Olivier DARNÉ,",
                            html.Br(),
                            "dans le cadre du Master 1 ECAP (2024–2025).",
                        ],
                        style={
                            "textAlign": "justify",  # Justification du texte
                            "fontSize": "14px",
                            "color": "white",
                            "margin": "0",
                        },
                    ),
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "height": "100%",
                    },
                ),
                style={
                    "height": "10vh",
                    "backgroundColor": "#6E8DBE",
                },
            )
        ),
    ],
    fluid=True,
)


# =========================================
# Callbacks pour les éléments interactifs
# =========================================


@callback(Output("legende-modeles", "children"), Input("filtre-modeles", "value"))
def update_legende_modeles(selected_modeles):
    if not selected_modeles or selected_modeles == ["all"]:
        modeles_a_afficher = modeles
    else:
        modeles_a_afficher = selected_modeles
    return construire_legende_modeles(modeles_a_afficher)


@callback(
    Output("filtre-modeles", "value"),
    Input("reset-filters", "n_clicks"),
    prevent_initial_call=True,
)
def reset_model_filter(n_clicks):
    return None


@callback(
    [
        Output("diag-alpha", "figure"),
        Output("diag-lambda", "figure"),
        Output("diag-nb-var", "figure"),
    ],
    [Input("filtre-modeles", "value")],
)
def update_dashboard(modele):

    hyperparametres_filtre = hyperparametres.copy()
    nb_variables_filtre = nb_variables.copy()

    if modele and modele != ["all"]:
        hyperparametres_filtre = hyperparametres_filtre[
            hyperparametres_filtre["Modele"].isin(modele)
        ]

        # On garde uniquement les colonnes correspondantes, en vérifiant leur présence
        colonnes_existantes = [col for col in modele if col in nb_variables.columns]
        colonnes_a_garder = ["Action"] + colonnes_existantes
        nb_variables_filtre = nb_variables_filtre[colonnes_a_garder]

    diag_alpha = diagramme_hyperparametres(
        hyperparametres_filtre,
        y_column="alpha",
        y_label="Valeur de alpha",
        title="Diagramme des valeurs de alpha",
        y_range=[0, 1.1],
    )

    diag_lambda = diagramme_hyperparametres(
        hyperparametres_filtre,
        y_column="lambda",
        y_label="Valeur de lambda",
        title="Diagramme des valeurs de lambda",
    )

    diag_nb_var = diagramme_nb_variables(nb_variables_filtre)

    return diag_alpha, diag_lambda, diag_nb_var


@callback(
    Output("etat-normalisation", "data"),
    Output("toggle-normalisation", "children"),
    Input("toggle-normalisation", "n_clicks"),
    State("etat-normalisation", "data"),
    prevent_initial_call=True,
)
def toggle_normalisation(n_clicks, is_normalized):
    new_state = not is_normalized
    button_text = (
        "Afficher les coefficients initiaux"
        if new_state
        else "Normaliser les coefficients"
    )

    return new_state, button_text


@callback(
    [
        Output("table-coefficients", "data"),
        Output("table-coefficients", "columns"),
        Output("table-coefficients", "style_data_conditional"),
        Output("table-coefficients", "style_header_conditional"),
    ],
    [Input("filtre-modeles", "value"), Input("etat-normalisation", "data")],
)
def update_table_coefficients(selected_modeles, is_normalized):
    filtered_data = coefficients.copy()

    if selected_modeles and selected_modeles != ["all"]:
        colonnes_a_conserver = ["Action"] + [
            col for col in selected_modeles if col in filtered_data.columns
        ]
        filtered_data = filtered_data[colonnes_a_conserver]

    # Appliquer normalisation si activée
    if is_normalized:
        norm_data = filtered_data.copy()
        for col in norm_data.columns:
            if col != "Action":
                total = norm_data[col].sum()
                if total != 0:
                    norm_data[col] = norm_data[col] / total
        display_data = norm_data.copy()
    else:
        display_data = filtered_data.copy()

    # Conserver les données numériques, pas de format_scientifique ici
    columns = [{"name": "Action", "id": "Action"}]
    for col in display_data.columns:
        if col != "Action":
            columns.append(
                {
                    "name": "",
                    "id": col,
                    "type": "numeric",
                    "format": Format(precision=2, scheme="e"),  # notation scientifique
                }
            )

    # Style conditionnel des données
    style_data_conditional = []
    for i, row in display_data.iterrows():
        for col in display_data.columns:
            if col == "Action":
                continue
            try:
                val = float(row[col])
            except:
                val = None

            color = (
                "#ff4d4d"
                if (val is None or val == 0.0 or math.isnan(val))
                else "#85e085"
            )
            style_data_conditional.append(
                {"if": {"row_index": i, "column_id": col}, "backgroundColor": color}
            )

    # Header coloré
    style_header_conditional = [
        {
            "if": {"column_id": col},
            "backgroundColor": couleurs_modeles.get(col, "#001F3F"),
            "color": "white",
        }
        for col in display_data.columns
        if col in couleurs_modeles
    ]

    return (
        display_data.to_dict("records"),
        columns,
        style_data_conditional,
        style_header_conditional,
    )


@callback(
    Output("bloc-performance", "children"),
    Input("filtre-modeles", "value"),
)
def update_graphiques_performance(modeles_selectionnes):
    return generer_graphiques_performance(performance, modeles_selectionnes)


if __name__ == "__main__":
    app.run(debug=True, port=8888, jupyter_mode="external")
