from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import History
from datetime import datetime
from . import db
import json
import plotly
import plotly.express as px
import CSVCleaner
import Transformer.workforce_transformer as workforce_transformer
import joblib

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/dash')
@login_required
def dashboard():
    # Rajouter peut-être le nombre de sociétés que j'ai dans ma base de données (comme ça je connais mon nombre de lignes)
    # Aller voir sur ce site l'image en dessous est pas mal https://www.octoboard.com/blog/tableau-de-bord-octoboard/

    df = CSVCleaner.graph_cleaner('/home/dorian/Python Linux/Projets Finaux/E1/company_siren50K.csv')
    df_temp = workforce_transformer.workforce_changer(df)

    # Graph One
    fig1 = px.pie(
        df_temp,
        names='workforce',
        title='Nombre de salariés')

    fig1.update_traces(hovertemplate='%{label}<br>Quantité : %{value}')

    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph Two
    fig2 = px.pie(
        df,
        names="category",
        title="Catégories d'entreprises")

    fig2.update_traces(hovertemplate='%{label}<br>Quantité : %{value}')

    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three

    fig3 = px.histogram(df, x='creation_date', title="Nombre d'entreprises créées par date.")

    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("dashboard.html", user=current_user, graph1JSON=graph1JSON, graph2JSON=graph2JSON,
                           graph3JSON=graph3JSON)


@views.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        df = CSVCleaner.csv_cleaner('/home/dorian/Python Linux/Projets Finaux/E1/company_siren50K.csv')
        # replacing categories values by numbers here because it could have messed up with the dashboard if the modification was done in CSVCleaner.py

        siren = request.form.get('siren')
        siren = siren.replace(' ', '')
        if siren in df['siren'].values:
            X = df.drop(
                ['siren','scoring'],
                axis=1)
            data = X.loc[df['siren'] == siren]  # Sélectionner les lignes correspondant au siren donné
            model_path = "modelV0DT.pkl"
            pred_model = joblib.load(model_path)
            prediction = pred_model.predict(data)

            #ajouter la probabilité
            if prediction == 0:
                flash('Le scoring attribué à ce siren est 0.')
            elif prediction == 1:
                flash('Le scoring attribué à ce siren est 1.')
            elif prediction == 2:
                flash('Le scoring attribué à ce siren est 2.')
            elif prediction == 3:
                flash('Le scoring attribué à ce siren est 3.')
            elif prediction == 4:
                flash('Le scoring attribué à ce siren est 4.')
            elif prediction == 5:
                flash('Le scoring attribué à ce siren est 5.')
            elif prediction == 6:
                flash('Le scoring attribué à ce siren est 6.')
            elif prediction == 7:
                flash('Le scoring attribué à ce siren est 7.')
            else:
                flash('La prédiction n\'a pas fonctionné')

            new_prediction = History(siren=siren, scoring=int(prediction), date=datetime.now(), user=current_user)
            db.session.add(new_prediction)
            db.session.commit()

        if len(siren) == 0:
            flash('Aucun SIREN n\'a été entré.')
        elif not siren.isdigit():
            flash('Le SIREN doit être seulement composé de chiffres.')
        elif len(siren) != 9:
            flash('Le SIREN doit contenir exactement 9 chiffres')
        elif siren not in df['siren'].values:
            flash('Le SIREN n\'existe pas en base.')

    return render_template("prediction.html", user=current_user)