# Global Markets Insights

### Análisis y Cálculo de metricas financieras de acuerdo a convenciones de mercado

> _"La hora optima de almuerzo, es a las 12 del día..."_

Master Branch deployment en producción @ https://global-markets-i.herokuapp.com/

### Instrucciones run local:
- correr archivo index.py en el _terminal_
- celdas bloqueadas en excel batch, password: _108_

<img src="https://github.com/claudio-oj/global-markets-i/blob/develop/assets/gmi_img_snapshot2.png" width=800 style="float: center; margin-right: 10px;" />

### Desarrollo Modular:

El **batch** recibe como input la data de bloomberg de precios que sube el middle office --> El **proceso batch** que corre 2am, transforma esa data en `fra1m` (_tasas FRA de 1 mes_) y produce la serie de tiempo de esas `fra1m` para cada uno de los 1 a 380 plazos, mas 18m y 24m, de la curva _money market_. (Y produce la `icam-os` ?)  
A primera hora de la mañana el cliente final inicia sesión en la **app** e interactua con la calculadora insertando valores en las tablas.

### To Do:
1. pasar dominio host de heroku a uno .cl http://ivdevs.com/blog/2017/05/17/personalizando-dominio-de-una-app-alojada-en-heroku/
2. ver donde inspeccionar _users log history_
3. **aumentar los dynos**
4. **bug**: fix funciones inestables calendario
5. **bug**: en `bbg_hist_dnlder_excel.xlsx` arreglar consulta bbg que rellene nan's con dato del dia anterior: icam 30yrs vino con nan's
6. **bug**: arreglar favicon. O decidir eliminar el x defecto de dash
7. Titulo header a `Klavika` font. Aprendear a incoporarlo al codigo.
8. **bug**: el calendario correcto para los _IR Swaps USD Libor_ es `settle holidays NY` , ahora estoy calculandolo con el calendario NY&STGO conjunto --> fix
9. **bug importante**: cada vez que _uso_ o _calculo_ un "precio explicito" i.e puntos, basis, icam, etc... --> **REDONDEAR** según convención.
10. limitar el ancho de `table1` para que en monitores anchos se compagine bien. y sean solo los graficos los que se extiendan
11. **bug importante**: en el grafico de arriba a la derecha muestra la última tasa fra con fecha `fec0`, siendo que debiese ser `fec1`. Idealmente arreglar antes del deploymente
12. Terminar table2: `dates`
13. Hacer grafico3, con la time series historia de la fra de la tabla2
14. Hacer la función corre _loop_, busca spreads baratos/caros
15. compaginar _row / columns_ satisfactoriamente
16. chequear que funcione bien el envio de excels del cliente

### To Do s terminados.
1. ~~agregar user y password~~
2. ~~crear pagina de inicio user y password, contacto~~
3. ~~remover banda superior graficos plotly~~
4. ~~integrar heroku CLI con Github~~
5. ~~storage memoria cache "puntos del dia"~~
6. ~~Desarrollar **widgets precios**~~
7. ~~**bug**: pestaña FX ptos, en la tabla html, al seleccionar celdas no editables se pega el cursor. Posible causa: _pifia_ en los **callbacks**, inconsistencia INPUT --> STATE --> OUTPUT. _pifia muy odiosa jaja_~~
8. ~~Desarrollo flujo **Batch** proceso o/n desde archivo `excel` bloomberg **TRABAJANDO EN ESTO**~~
9 ~~Documentación "funciones CO", para hacer más entendible el codigo~~
10. ~~Modificar la lectura de data inicial, de la data dummy que cree originalmente --> al proceso batch~~
11. ~~acordarnos de modificar el email a gmi.usdclp@gmail.com, contraseña gmail *tobrjciaqyuzywkq*~~


### Metodología de Desarrollo:
- master branch (producción), develop branch, features branches  
  <img src="http://featureflags.io/wp-content/uploads/2018/03/featurebranchingwithflags.jpg" width=700 style="float: center; margin-right: 10px;" />

### Ideas de Mejoras para Versiones Futuras
1. ~~en Pestaña FX ptos: permitir input manual en tabla html de `ilib`, `tcs` ~~
2. eliminar post batch las variables que ocupa el batch. Para ocupar menos memoria durante el día, cuando el usuario final ocupa la calculadora.
3. calcular los _puntos>2yrs_ en el df inicial, para `table1`
4. En el gráfico fra transversal incluir `1w`,`2w`
5. Para impedir *typos* en las tablas. Y que el usuario pierda información. Solución: --> que en las funciones update dentro de los callbacks, se pise cada vez las columnas que no debieran ser editables

### Explicaciones Batch
1. los archivos **`p_*.pkl`** son los pickle con los df de cada dia, de los precios descargados de bloomberg, con sus fechas respectivas y calculo de carry days en base a la comvención de calendario de mercado.

#### Flujo Batch
<img src="https://github.com/claudio-oj/global-markets-i/blob/develop/batch/gmi_batch.png" width=900 style="float: center; margin-right: 10px;" />

<!-- https://en.wikipedia.org/wiki/Web_colors#X11_color_names -->

##### recordatorio graficos side-by-side
""" https://community.plot.ly/t/two-graphs-side-by-side/5312 """
