# Global Markets Insights
### Análisis y Cálculo de metricas financieras de acuerdo a convenciones de mercado

> _"La hora optima de almuerzo, es a las 12 del día..."_

### Instrucciones:
correr archivo index.py en el _terminal_

<img src="https://github.com/claudio-oj/global-markets-i/blob/master/assets/gmi_img_snapshot2.png" width=800 style="float: center; margin-right: 10px;" />


### Desarrollo Modular:
El **batch** recibe como input la data de bloomberg de precios que sube el middle office --> El **proceso batch** que corre 2am, transforma esa data en  `fra1m` (_tasas FRA de 1 mes_) y produce la serie de tiempo de esas `fra1m` para cada uno de los 1 a 380 plazos, mas 18m y 24m, de la curva _money market_.  (Y produce la `icam-os` ?)  
A primera hora de la mañana el cliente final inicia sesión en la **app** e interactua con la calculadora insertando valores en las tablas.

### To Do:
1. pasar dominio host de heroku a www.binaryanalytics.cl/gmi
2. ~~agregar user y password~~
3. ver donde inspeccionar _users log history_
4. ~~crear pagina de inicio user y password, contacto~~
5. ~~remover banda superior graficos plotly~~
6. integrar heroku CLI con Github
7. aumentar los dynos
8. storage memoria cache "puntos del dia"


* ~~analizar si vale la pena modificar callbacks para q sea todo pandas~~
* desarrollar mini calculadoras en base a fra s. desde * curva cero fra s
* crear proceso o/n desde archivo bloomberg **TRABAJANDO EN ESTO**
* ~~agregar div Markdown abajo al medio: copyright, contacto, disclosures.~~
  
     
### Metodología de Desarrollo:
- master branch (producción), develop branch, features branches