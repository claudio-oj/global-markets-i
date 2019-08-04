import dash_core_components as dcc
import dash_html_components as html

from app import app


layout = html.Div(
	className='nine columns offset-by-one',
	children=[
		html.Br(),
		html.Br(),
		html.Div(
			html.Img(src='https://static.wixstatic.com/media/963559_aa62287269154585a1a8c607ecf64fc4~mv2.gif',
					 style={'width': '125px'}),
			style={'textAlign': 'center'},
		),
		html.H2("Global-Markets Insights", style={'textAlign':'center'}),
		html.P("Interbank markets financial data processing in the back-end ... for friendly assessment in the front-end... ",
			   style={
				   'textAlign':'center',
				   'font-style': 'italic',
			   }
		),
		dcc.Markdown('''---'''),

		html.Br(),
		# html.Br(),
		# html.Br(),

		html.Div(
			style={'display':'flex','justify-content':'center','fontSize':13}, # http://howtocenterincss.com/
			children=[dcc.Markdown('''
Host| [BinaryAnaytics.cl](http://www.BinaryAnaytics.cl) | |
:-------- | :---------: | :---------:
Website | [global-markets-i.herokuapp.com](https://global-markets-i.herokuapp.com/) | |
Latest Release| v2 beta Chile | 05-Aug-2019 |
Tutorial | [binaryanalytics.cl/gmi-tutorial](https://www.binaryanalytics.cl/gmi-tutorial) | password: *binaryanalytics*
Requirements | Google Chrome desktop > 13' | |
| Contact | [contacto@binaryanalytics.cl](mailto:contacto@binaryanalytics.cl) | |
'''
					)],
		),

		html.Br(),
		html.Br(),
# 		dcc.Markdown('''
#
# ##### FX
#
# > Variable | Definición
# > :--------: | ---------
# > `t` | tenor
# > `ptslcl`  | puntos forward locales
# > `ptsos`| puntos forward off shore
# > `icam` | Interest Rate Swap Camara local
# > `irslibor` | Interest Rate Swap USD libor 3 months
# > `bsis` | Cross Currency Swap USD.CLP basis
# > `iptos` | puntos forward locales **implicitos** en `icam` + `irslibor` + `bsis`
# > `ibsis` | basis **implicitos** en `icam` + `irslibor` + `ptslcl`
# > `icam-os`| tasa de interés camara sintetica u off-shore. Tasa calculada en base a `ptos` + `irslibor`
# > `fra`| tasa de interés forward en base a la curva `icam-os`
# > `os-lcl spread`| Spread: `icam-os` - `icam`. Es el *precio relativo* de los puntos forward
# > `mean spread`| promedio historico (1 año) de `os-lcl spread`
# > `rank_tod` | ranking percentil tasa fra implicita en el spread cotizado, respecto a la curva **de hoy**
# > `rank_his` | ranking percentil tasa fra implicita en el spread cotizado, respecto a su propia historia, **serie de tiempo (1 año)**
# '''),
#
# 		html.Br(),
# 		dcc.Markdown('''
# ##### Basis
# >en desarrollo...
# '''
# 		),
# 		html.Br(),
# 		dcc.Markdown('''
# ##### IR cam
# >en desarrollo...
# '''
# 		),
# 		html.Br(),
# 		dcc.Markdown('''
# ##### Sovereign Bonds
# >en desarrollo...
# '''
# 		),
# 		html.Br(),
# 		dcc.Markdown('''
# ##### Inflation
# >en desarrollo...
# '''
# 		),
# 		html.Br(),
# 		dcc.Markdown('''
# ##### Middle-Office
# >en desarrollo...
# '''
# 		),
# 		html.Br(),
# 		html.Br(),
	],
)

