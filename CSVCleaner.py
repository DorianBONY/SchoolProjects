import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import os


def graph_cleaner(csv_file):
    df = pd.read_csv(csv_file, delimiter=";")
    df.copy()

    df.dropna(subset=['category'], inplace=True)
    df.dropna(subset=['workforce'], inplace=True)

    return df


def csv_cleaner(csv_file):
    df = pd.read_csv(csv_file, delimiter=";")
    df.copy()

    df['siren'] = df['siren'].astype(str).str.zfill(9)
    df.drop(['siret', 'main_activity_nomenclature', 'year_category', 'date_closing_Exer', 'insee_administratif_status',
             'legal_category_code', 'last_insee_update', 'turnover_date', 'send_to_marketing_automation', 'is_closed',
             'lei_renewal_date', 'lei_subscription_date', 'lei_number', 'eori_number'], axis=1, inplace=True)

    df = df.dropna()

    # Supprimer les chiffres après le nom de la ville
    df['city_name'] = df['city_name'].str.replace(r'\d+', '')
    df['city_name'] = df['city_name'].str.replace('EME', '')
    # Afficher les valeurs uniques dans la colonne "city_name"
    unique_cities = df['city_name'].unique()

    df['creation_year'] = df['creation_date'].str.extract(r'(\d{4})')
    df.drop('creation_date', axis=1, inplace=True)

    # Obtenir les dix valeurs les plus présentes dans la colonne 'creation_year'
    top_10 = [x for x in df['creation_year'].value_counts().sort_values(ascending=False).head(10).index]

    # Créer des colonnes binaires pour les dix valeurs les plus présentes
    for label in top_10:
        new_label = f'creation_year_{label}'
        df[new_label] = np.where(df['creation_year'] == label, 1, 0)

    # Créer une colonne 'other' pour les valeurs qui ne font pas partie des dix premières
    df['creation_year_other'] = np.where(df['creation_year'].isin(top_10), 0, 1)

    # Supprimer la colonne 'creation_year' du DataFrame
    df.drop('creation_year', axis=1, inplace=True)

    df['start_date_year'] = df['start_date'].str.extract(r'(\d{4})')
    df.drop('start_date', axis=1, inplace=True)

    # Obtenir les dix valeurs les plus présentes dans la colonne 'creation_year'
    top_5 = [x for x in df['start_date_year'].value_counts().sort_values(ascending=False).head(5).index]

    # Créer des colonnes binaires pour les dix valeurs les plus présentes
    for label in top_5:
        new_label = f'start_date_year_{label}'
        df[new_label] = np.where(df['start_date_year'] == label, 1, 0)

    # Créer une colonne 'other' pour les valeurs qui ne font pas partie des dix premières
    df['start_date_year_other'] = np.where(df['start_date_year'].isin(top_5), 0, 1)

    # Supprimer la colonne 'creation_year' du DataFrame
    df.drop('start_date_year', axis=1, inplace=True)

    # df['category_type'] = pd.factorize(df.category)[0]
    # df.drop('category', axis=1, inplace=True)

    # Instanciation de l'encodeur OneHotEncoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    # Ajustement et transformation des données
    category_encoded = encoder.fit_transform(df[['category']])

    # Suppression de la colonne 'category' du DataFrame
    df.drop('category', axis=1, inplace=True)

    # Création d'un DataFrame à partir des données encodées
    encoded_df = pd.DataFrame(
        category_encoded,
        columns=[f'category_{category}' for category in encoder.categories_[0]]
    )

    # Concaténation du DataFrame encodé avec le DataFrame original
    df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

    # df['workforce_type'] = pd.factorize(df.workforce)[0]
    # df.drop('workforce', axis=1, inplace=True)

    # Obtenir les dix valeurs les plus présentes dans la colonne 'creation_year'
    top_10 = [x for x in df['workforce'].value_counts().sort_values(ascending=False).head(10).index]

    # Créer des colonnes binaires pour les dix valeurs les plus présentes
    for label in top_10:
        new_label = f'workforce_{label}'
        df[new_label] = np.where(df['workforce'] == label, 1, 0)

    # Créer une colonne 'other' pour les valeurs qui ne font pas partie des dix premières
    df['workforce_other'] = np.where(df['workforce'].isin(top_10), 0, 1)

    # Supprimer la colonne 'creation_year' du DataFrame
    df.drop('workforce', axis=1, inplace=True)

    # df['lei_company_status_type'] = pd.factorize(df.lei_company_status)[0]
    # df.drop('lei_company_status', axis=1, inplace=True)

    # Instanciation de l'encodeur OneHotEncoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    # Ajustement et transformation des données
    status_encoded = encoder.fit_transform(df[['lei_company_status']])

    # Suppression de la colonne 'lei_company_status' du DataFrame
    df.drop('lei_company_status', axis=1, inplace=True)

    # Création d'un DataFrame à partir des données encodées
    encoded_df = pd.DataFrame(
        status_encoded,
        columns=[f'lei_company_status_{status}' for status in encoder.categories_[0]]
    )

    # Concaténation du DataFrame encodé avec le DataFrame original
    df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

    # df['lei_registration_status_type'] = pd.factorize(df.lei_registration_status)[0]
    # df.drop('lei_registration_status', axis=1, inplace=True)

    # Instanciation de l'encodeur OneHotEncoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    # Ajustement et transformation des données
    status_encoded = encoder.fit_transform(df[['lei_registration_status']])

    # Suppression de la colonne 'lei_registration_status' du DataFrame
    df.drop('lei_registration_status', axis=1, inplace=True)

    # Création d'un DataFrame à partir des données encodées
    encoded_df = pd.DataFrame(
        status_encoded,
        columns=[f'lei_registration_status_{status}' for status in encoder.categories_[0]]
    )

    # Concaténation du DataFrame encodé avec le DataFrame original
    df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

    # df['city_name_type'] = pd.factorize(df.city_name)[0]
    # df.drop('city_name', axis=1, inplace=True)

    # Obtenir les dix valeurs les plus présentes dans la colonne 'creation_year'
    top_5 = [x for x in df['city_name'].value_counts().sort_values(ascending=False).head(5).index]

    # Créer des colonnes binaires pour les dix valeurs les plus présentes
    for label in top_5:
        new_label = f'city_name_{label}'
        df[new_label] = np.where(df['city_name'] == label, 1, 0)

    # Créer une colonne 'other' pour les valeurs qui ne font pas partie des dix premières
    df['city_name_other'] = np.where(df['city_name'].isin(top_5), 0, 1)

    # Supprimer la colonne 'creation_year' du DataFrame
    df.drop('city_name', axis=1, inplace=True)

    # df['city_code_type'] = pd.factorize(df.city_code)[0]
    # df.drop('city_code', axis=1, inplace=True)

    # Obtenir les dix valeurs les plus présentes dans la colonne 'creation_year'
    top_10 = [x for x in df['city_code'].value_counts().sort_values(ascending=False).head(10).index]

    # Créer des colonnes binaires pour les dix valeurs les plus présentes
    for label in top_10:
        new_label = f'city_code_{label}'
        df[new_label] = np.where(df['city_code'] == label, 1, 0)

    # Créer une colonne 'other' pour les valeurs qui ne font pas partie des dix premières
    df['city_code_other'] = np.where(df['city_code'].isin(top_10), 0, 1)

    # Supprimer la colonne 'creation_year' du DataFrame
    df.drop('city_code', axis=1, inplace=True)

    # df['capital_type_bis'] = pd.factorize(df.capital_type)[0]
    # df.drop('capital_type', axis=1, inplace=True)

    # Instanciation de l'encodeur OneHotEncoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    # Ajustement et transformation des données
    status_encoded = encoder.fit_transform(df[['capital_type']])

    # Suppression de la colonne 'lei_registration_status' du DataFrame
    df.drop('capital_type', axis=1, inplace=True)

    # Création d'un DataFrame à partir des données encodées
    encoded_df = pd.DataFrame(
        status_encoded,
        columns=[f'capital_type_{status}' for status in encoder.categories_[0]]
    )

    # Concaténation du DataFrame encodé avec le DataFrame original
    df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

    # df['main_activity_type'] = pd.factorize(df.main_activity)[0]
    # df.drop('main_activity', axis=1, inplace=True)

    # Obtenir les dix valeurs les plus présentes dans la colonne 'creation_year'
    top_5 = [x for x in df['main_activity'].value_counts().sort_values(ascending=False).head(5).index]

    # Créer des colonnes binaires pour les dix valeurs les plus présentes
    for label in top_5:
        new_label = f'main_activity_{label}'
        df[new_label] = np.where(df['main_activity'] == label, 1, 0)

    # Créer une colonne 'other' pour les valeurs qui ne font pas partie des dix premières
    df['main_activity_other'] = np.where(df['main_activity'].isin(top_5), 0, 1)

    # Supprimer la colonne 'creation_year' du DataFrame
    df.drop('main_activity', axis=1, inplace=True)

    return df
