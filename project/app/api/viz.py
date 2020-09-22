from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

router = APIRouter()

@router.get('/viz/usa')
async def viz():
    df = pd.read_csv('https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-DS/FEAT/police-violence-incidents-database/Data/pv_incidents.csv')
    # df['text'] = df['airport'] + '' + df['city'] + ', ' + df['state'] + '' + 'Arrivals: ' + df['cnt'].astype(str)

    fig = go.Figure(data=go.Scattergeo(
    lon = df['LONGITUDE'],
    lat = df['LATITUDE'],
    text = df['name'],
    # mode = 'markers',
    # marker_color = df['cnt'],
    ))

    fig.update_layout(
        title = 'POLICE INCIDENTS',
        geo_scope='usa',
    )
    
    return fig.to_json()
    