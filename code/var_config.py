ALL_VAR_CONFIG = {
    "happiness_score": {
        "color": "#f1c40f",
        "label": "Score de Bonheur"
    },
    "gdp_per_capita": {
        "color": "#27ae60",
        "label": "PIB par habitant"
    },
    "gdp_log": {
        "color": "#27ae60",
        "label": "PIB par habitant"
    },
    "social_support": {
        "color": "#2980b9",
        "label": "Soutien social"
    },
    "healthy_life_expectancy": {
        "color": "#c0392b",
        "label": "Espérance de vie"
    },
    "life_expectancy": {
        "color": "#c0392b",
        "label": "Espérance de vie"
    },
    "freedom_to_choose": {
        "color": "#8e44ad",
        "label": "Liberté de faire des choix"
    },
    "generosity": {
        "color": "#16a085",
        "label": "Générosité de la population"
    },
    "corruption_perception": {
        "color": "#7f8c8d",
        "label": "Perception de la corruption"
    },
    "cpi": {
        "color": "#7f8c8d",
        "label": "Indice de perception de la corruption"
    },
    "unemployment_rate": {
        "color": "#d35400",
        "label": "Taux de chômage"
    },
    "active_population_rate": {
        "color": "#a87420",
        "label": "Pourcentage de la population active (15–64 ans)"
    },
    "urban_population_rate": {
        "color": "#3498db",
        "label": "Taux d'urbanisation"
    },
    "voice_accountability": {
        "color": "#db99f5",
        "label": "Libertés publiques et participation"
    },
    "government_effectiveness": {
        "color": "#92143e",
        "label": "Efficacité du gouvernement"
    },
    "co2_emissions_per_capita": {
        "color": "#000000",
        "label": "Émissions de CO₂ par habitant"
    },
    "temperature_change_from_ghg": {
        "color": "#24ffbd",
        "label": "Variation de température due aux gaz à effet de serre"
    },
}

def make_config(active_vars):
    """
    active_vars : liste des variables à utiliser.
    Retourne (VAR_CONFIG, COLS_NUM).
    """
    config = {v: ALL_VAR_CONFIG[v] for v in active_vars}
    return config, active_vars