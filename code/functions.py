import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def clean_name(x: str) -> str:
    """Harmonise les noms de pays pour toutes les sources externes."""
    if pd.isna(x):
        return x
    x = x.strip()

    replacements = {
        "Czech Republic": "Czechia",
        "Macedonia": "North Macedonia",
        "Turkey": "Turkiye",
        "Türkiye": "Turkiye",
        "Palestine": "State of Palestine",
        "Côte d'Ivoire": "Ivory Coast",
        "Cote d'Ivoire": "Ivory Coast",
        "Côte d’Ivoire": "Ivory Coast",
        "Viet Nam": "Vietnam",
        "Russian Federation": "Russia",
        "Bahamas, The": "Bahamas",
        "Bolivia (Plurinational State of)": "Bolivia",
        "Gambia, The": "Gambia",
        "Republic of Korea": "South Korea",
        "Korea, Rep.": "South Korea",
        "Korea, Dem. Rep.": "North Korea",
        "Korea, Dem. People's Rep.": "North Korea",
        "Egypt, Arab Rep.": "Egypt",
        "Hong Kong S.A.R. of China": "Hong Kong",
        "Hong Kong SAR, China": "Hong Kong",
        "China, Hong Kong Special Administrative Region": "Hong Kong",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "United States of America": "United States",
        "Taiwan Province of China": "Taiwan",
        "Kyrgyz Republic": "Kyrgyzstan",
        "Congo (Kinshasa)": "Democratic Republic of the Congo",
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        "Democratic Republic of Congo": "Democratic Republic of the Congo",
        "Congo (Brazzaville)": "Republic of the Congo",
        "Congo, Rep.": "Republic of the Congo",
        "Republic of Congo": "Republic of the Congo",
        "Slovak Republic": "Slovakia",
        "Iran, Islamic Rep.": "Iran",
        "Iran (Islamic Republic of)": "Iran",
        "Venezuela, RB": "Venezuela",
        "Venezuela (Bolivarian Republic of)": "Venezuela",
        "Lao PDR": "Laos",
        "Syrian Arab Republic": "Syria",
        "Somalia, Fed. Rep.": "Somalia",
        "Swaziland": "Eswatini",
        "Trinidad & Tobago": "Trinidad and Tobago",
        "Palestinian Territories": "State of Palestine",
        "Argelia": "Algeria",
        "Republic of Moldova": "Moldova",
        "United Republic of Tanzania": "Tanzania",
    }

    return replacements.get(x, x)


def report_missing_by_country(
    df: pd.DataFrame,
    var: str,
    label: str | None = None
) -> None:
    """
    Affiche pour une variable donnée la liste des pays qui ont des NA,
    avec les années manquantes.
    """
    label = label or var
    mask = df[var].isna()
    missing_rows = df[mask]

    if missing_rows.empty:
        print(f"Aucune valeur manquante pour {label}.")
        return

    missing_countries = sorted(missing_rows["country"].unique())
    print(f"Pays sans {label} :")
    for country in missing_countries:
        years_missing = (
            missing_rows[missing_rows["country"] == country]["year"]
            .sort_values()
            .unique()
        )
        years_str = ", ".join(str(int(y)) for y in years_missing)
        print(f"- {country} (années manquantes : {years_str})")

    print("\nNombre total :", len(missing_countries))


def download_wdi(indicator: str, start: int = 2015, end: int = 2023) -> pd.DataFrame:
    """
    Télécharge un indicateur WDI pour tous les pays et années [start, end].
    Retourne un DataFrame avec colonnes : country, year, <indicator>.
    """
    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/"
        f"{indicator}?format=json&per_page=20000"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()[1]

    df = pd.DataFrame(data)

    # extraire le nom du pays
    df["country"] = df["country"].apply(
        lambda x: x["value"] if isinstance(x, dict) else x
    )
    df["country"] = df["country"].apply(clean_name)

    df = df.rename(columns={
        "date": "year",
        "value": indicator,
    })

    df["year"] = df["year"].astype(int)
    df = df[df["year"].between(start, end)]

    return df


def plot_profil(
    data: pd.DataFrame,
    variable: str,
    entity_name: str,
    folder_path: str,
    var_config: dict,
    year_min: int = 2015,
    year_max: int = 2023,
) -> None:
    """
    Génère et sauvegarde un graphique d'évolution pour une variable donnée.
    Utilise la couleur et le label définis dans var_config.
    """
    os.makedirs(folder_path, exist_ok=True)

    data = data[(data["year"] >= year_min) & (data["year"] <= year_max)]
    if data.empty:
        return
    data = data.sort_values("year")

    plt.figure(figsize=(10, 6))

    config = var_config.get(variable, {"color": "#333333", "label": variable})
    color = config["color"]
    label = config["label"]

    sns.lineplot(
        data=data,
        x="year",
        y=variable,
        marker="o",
        markersize=8,
        linewidth=2.5,
        color=color,
    )
    plt.title(f"Évolution : {label} - {entity_name}", fontsize=14, fontweight="bold")
    plt.xlabel("Année", fontsize=12)
    plt.ylabel(label, fontsize=12)
    plt.xticks(range(year_min, year_max + 1))
    plt.grid(True, linestyle="--", alpha=0.7)

    safe_entity = (
        entity_name.replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("'", "")
        .replace("/", "_")
    )
    if entity_name == "Moyenne mondiale":
        filename = f"mean_{variable}.png"
    else:
        filename = f"{safe_entity}_{variable}.png"

    plt.savefig(os.path.join(folder_path, filename), dpi=100)
    plt.close()


def generate_global_profiles(
    df: pd.DataFrame,
    cols_num: list[str],
    var_config: dict,
    profil_root: str,
    year_min: int = 2015,
    year_max: int = 2023,
) -> None:
    """
    Génère les graphiques pour la moyenne mondiale.
    Même résultat qu'avant, mais on filtre la plage d'années une seule fois.
    """
    path = os.path.join(profil_root, "global")
    os.makedirs(path, exist_ok=True)

    df_sub = df[(df["year"] >= year_min) & (df["year"] <= year_max)]
    df_global = (
        df_sub.groupby("year")[cols_num]
        .mean(numeric_only=True)
        .reset_index()
    )

    for var in cols_num:
        plot_profil(df_global, var, "Moyenne mondiale", path, var_config, year_min, year_max)


def generate_regional_profiles(
    df: pd.DataFrame,
    cols_num: list[str],
    var_config: dict,
    profil_root: str,
    year_min: int = 2015,
    year_max: int = 2023,
) -> None:
    """
    Génère les graphiques pour la moyenne par région.
    Optimisé : on agrège une seule fois par (region, year).
    """
    df_sub = df[(df["year"] >= year_min) & (df["year"] <= year_max)]
    df_reg_all = (
        df_sub
        .groupby(["region", "year"])[cols_num]
        .mean(numeric_only=True)
        .reset_index()
    )

    regions = df_reg_all["region"].dropna().unique()

    for region in regions:
        safe_name = region.replace(" ", "_").replace("/", "_")
        path = os.path.join(profil_root, "region", safe_name)
        os.makedirs(path, exist_ok=True)

        df_region = df_reg_all[df_reg_all["region"] == region]

        for var in cols_num:
            plot_profil(df_region, var, region, path, var_config, year_min, year_max)


def generate_country_profiles(
    df: pd.DataFrame,
    cols_num: list[str],
    var_config: dict,
    profil_root: str,
    year_min: int = 2015,
    year_max: int = 2023,
    countries: list[str] | None = None,  
) -> None:
    """
    Génère les graphiques pour chaque pays individuellement.

    - Si `countries` est None : tous les pays du DataFrame.
    - Sinon : uniquement les pays de la liste (ignorant ceux non présents).
    """
    df_sub = df[(df["year"] >= year_min) & (df["year"] <= year_max)]

    if countries is None:
        countries_list = df_sub["country"].dropna().unique()
    else:
        existing = set(df_sub["country"].dropna().unique())
        countries_list = [c for c in countries if c in existing]

    for country in countries_list:
        safe_name = (
            country.replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("'", "")
            .replace("/", "_")
        )
        path = os.path.join(profil_root, "country", safe_name)
        os.makedirs(path, exist_ok=True)

        df_country = df_sub[df_sub["country"] == country]
        if df_country.empty:
            continue

        for var in cols_num:
            plot_profil(df_country, var, country, path, var_config, year_min, year_max)
