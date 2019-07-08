# Global Markets Insights

### Análisis y Cálculo de metricas financieras de acuerdo a convenciones de mercado

> _"La hora optima de almuerzo, es a las 12 del día..."_

Master Branch deployment en producción @ https://global-markets-i.herokuapp.com/

**Instrucciones run local**: correr archivo index.py en el _terminal_

<img src="https://github.com/claudio-oj/global-markets-i/blob/develop/assets/gmi_img_snapshot2.png" width=800 style="float: center; margin-right: 10px;" />

### Desarrollo Modular:

El **batch** recibe como input la data de bloomberg de precios que sube el middle office --> El **proceso batch** que corre 2am, transforma esa data en `fra1m` (_tasas FRA de 1 mes_) y produce la serie de tiempo de esas `fra1m` para cada uno de los 1 a 380 plazos, mas 18m y 24m, de la curva _money market_. (Y produce la `icam-os` ?)  
A primera hora de la mañana el cliente final inicia sesión en la **app** e interactua con la calculadora insertando valores en las tablas.

### To Do:

1. pasar dominio host de heroku a www.binaryanalytics.cl/gmi
2. ~~agregar user y password~~
3. ver donde inspeccionar _users log history_
4. ~~crear pagina de inicio user y password, contacto~~
5. ~~remover banda superior graficos plotly~~
6. ~~integrar heroku CLI con Github~~
7. aumentar los dynos
8. storage memoria cache "puntos del dia"
9. Desarrollar **widgets precios**
10. **bug**: fix funciones inestables calendario
11. **bug**: en `bbg_hist_dnlder_excel.xlsx` arreglar consulta bbg que rellene nan's con dato del dia anterior: icam 30yrs vino con nan's
12. **bug**: pestaña FX ptos, en la tabla html, al seleccionar celdas no editables se pega el cursor. Posible causa: _pifia_ en los **callbacks**, inconsistencia INPUT --> STATE --> OUTPUT. _pifia muy odiosa jaja_
13. **bug**: arreglar favicon. O decidir eliminar el x defecto de dash
14. Titulo header a `Klavika` font. APrendear a incoporarlo al codigo.
15. Desarrollo flujo **Batch** proceso o/n desde archivo `excel` bloomberg **TRABAJANDO EN ESTO**
16. Documentación "funciones CO", para hacer más entendible el codigo
17. **bug**: el calendario correcto para los _IR Swaps USD Libor_ es `settle holidays NY` , ahora estoy calculandolo con el calendario NY&STGO conjunto --> fix
18. Modificar la lectura de data inicial, de la data dummy que cree originalmente --> al proceso batch

- ~~analizar si vale la pena modificar callbacks para q sea todo pandas~~
- desarrollar mini calculadoras en base a fra s. desde \* curva cero fra s
- **TRABAJANDO EN ESTO**: crear proceso o/n desde archivo bloomberg
- ~~agregar div Markdown abajo al medio: copyright, contacto, disclosures.~~

### Metodología de Desarrollo:

- master branch (producción), develop branch, features branches  
  <img src="http://featureflags.io/wp-content/uploads/2018/03/featurebranchingwithflags.jpg" width=700 style="float: center; margin-right: 10px;" />

### Ideas de Mejoras para Versiones Futuras

1. en Pestaña FX ptos: permitir input manual en tabla html de `ilib`, `tcs`
2. eliminar post batch las variables que ocupa el batch. Para ocupar menos memoria durante el día, cuando el usuario final ocupa la calculadora.

### Explicaciones Batch

1. los archivos **`p_*.pkl`** son los pickle con los df de cada dia, de los precios descargados de bloomberg, con sus fechas respectivas y calculo de carry days en base a la comvención de calendario de mercado.

#### Flujo Batch

<img src="https://github.com/claudio-oj/global-markets-i/blob/develop/batch/gmi_batch.png" width=900 style="float: center; margin-right: 10px;" />

<!-- https://en.wikipedia.org/wiki/Web_colors#X11_color_names -->
