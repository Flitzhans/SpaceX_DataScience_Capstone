{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "74f35213",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8050/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x262fbd66540>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# spacex_dash_app.py\n",
    "import pandas as pd\n",
    "import dash\n",
    "from dash import dcc, html\n",
    "from dash.dependencies import Input, Output\n",
    "import plotly.express as px\n",
    "\n",
    "spacex_df = pd.read_csv(\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv\")\n",
    "max_payload = spacex_df['Payload Mass (kg)'].max()\n",
    "min_payload = spacex_df['Payload Mass (kg)'].min()\n",
    "\n",
    "app = dash.Dash(__name__)\n",
    "app.layout = html.Div([\n",
    "    html.H1('SpaceX Launch Records Dashboard', style={'textAlign':'center'}),\n",
    "    dcc.Dropdown(id='site-dropdown',\n",
    "        options=[{'label':'All Sites','value':'ALL'}] +\n",
    "                [{'label':s,'value':s} for s in spacex_df['Launch Site'].unique()],\n",
    "        value='ALL', placeholder=\"Select a Launch Site\", searchable=True),\n",
    "    html.Br(),\n",
    "    html.Div(dcc.Graph(id='success-pie-chart')),\n",
    "    html.Br(),\n",
    "    html.P(\"Payload range (Kg):\"),\n",
    "    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,\n",
    "                    marks={i: str(i) for i in range(0, 10001, 2500)},\n",
    "                    value=[min_payload, max_payload]),\n",
    "    html.Div(dcc.Graph(id='success-payload-scatter-chart')),\n",
    "])\n",
    "\n",
    "@app.callback(Output('success-pie-chart','figure'),\n",
    "              Input('site-dropdown','value'))\n",
    "def get_pie_chart(entered_site):\n",
    "    if entered_site == 'ALL':\n",
    "        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')\n",
    "    else:\n",
    "        filtered = spacex_df[spacex_df['Launch Site'] == entered_site]\n",
    "        fig = px.pie(filtered, names='class', title=f'Success vs Failed for {entered_site}')\n",
    "    return fig\n",
    "\n",
    "@app.callback(Output('success-payload-scatter-chart','figure'),\n",
    "              [Input('site-dropdown','value'), Input('payload-slider','value')])\n",
    "def get_scatter_chart(entered_site, payload):\n",
    "    filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) &\n",
    "                         (spacex_df['Payload Mass (kg)'] <= payload[1])]\n",
    "    if entered_site == 'ALL':\n",
    "        fig = px.scatter(filtered, x='Payload Mass (kg)', y='class',\n",
    "                         color='Booster Version Category', title='Payload vs Outcome for All Sites')\n",
    "    else:\n",
    "        filtered = filtered[filtered['Launch Site'] == entered_site]\n",
    "        fig = px.scatter(filtered, x='Payload Mass (kg)', y='class',\n",
    "                         color='Booster Version Category', title=f'Payload vs Outcome for {entered_site}')\n",
    "    return fig\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "base",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
