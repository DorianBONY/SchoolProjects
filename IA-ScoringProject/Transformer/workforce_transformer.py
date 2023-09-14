def workforce_changer(df):
    df['workforce'] = df['workforce'].replace('00', '0 salarié')
    df['workforce'] = df['workforce'].replace('01', '1 ou 2 salariés')
    df['workforce'] = df['workforce'].replace('02', '3 à 5 salariés')
    df['workforce'] = df['workforce'].replace('03', '6 à 9 salariés')
    df['workforce'] = df['workforce'].replace('11', '10 à 19 salariés')
    df['workforce'] = df['workforce'].replace('12', '20 à 49 salariés')
    df['workforce'] = df['workforce'].replace('21', '50 à 99 salariés')
    df['workforce'] = df['workforce'].replace('22', '100 à 199 salariés')
    df['workforce'] = df['workforce'].replace('31', '200 à 249 salariés')
    df['workforce'] = df['workforce'].replace('32', '250 à 499 salariés')
    df['workforce'] = df['workforce'].replace('41', '500 à 999 salariés')
    df['workforce'] = df['workforce'].replace('42', '1000 à 1999 salariés')
    df['workforce'] = df['workforce'].replace('51', '2000 à 4999 salariés')
    df['workforce'] = df['workforce'].replace('52', '5000 à 9999 salariés')
    df['workforce'] = df['workforce'].replace('53', '10000 et + salariés')
    df['workforce'] = df['workforce'].replace('NN', 'Unité non employeuse')
    
    return df