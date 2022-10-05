import streamlit as st
import pandas as pd 
from PIL import Image
from scipy import stats
import numpy as np

image1 = Image.open('Histograma_.png')
image2 = Image.open('Boxplot_.png')
image3 = Image.open('Heatmap_.png')


df = pd.read_csv('https://raw.githubusercontent.com/labeconometria/MLxE/main/proyectos2do/datasets3.csv')

st.title('Proyecto 6 - Calidad del Agua')
st.write('Nombre : Hugo Fonseca\n')
st.subheader('**Introducción**')
st.write(
    """
    En este proyecto se desarrollar un análisis de una tabla sobre variables que evalúan aspectos \
    relacionados con la calidad del agua, se realizara una exploración, limpieza y después tratamiento \
    de datos con herramientas estadísticas y de probabilidad. 
    """
)
st.subheader('**Exploración Inicial de los Datos**')

st.write("""
Para la exploración inicial de los datos se puede comentar las variables que aparecen en la tabla, visualicemos\
 una porción de la tabla para observar cada una de estas, tenga en cuenta que todas están relacionada con aspectos\
 sobre la calidad del agua, sin embargo la última ‘Potability’ hace referencia con 1 a que el agua es potable y con 0 a que no lo es.
"""
)


st.table(df.head())

st.write("""
Realizando una exploración rápida de estos datos nos podemos dar cuenta a simple vista de problemas como missing values,\
 de manera que a continuación se solucionaran diferentes problemas en la sección de la limpieza de datos, sin embargo, podemos\
 identificar en la siguiente tabla el porcentaje de missing values por variable.
""")

tabla_info = pd.DataFrame([{col: str(round(((df[col].isna().sum())/len(df))*100,2))+' %' for col in df.columns}]).T
tabla_info.columns = ['Porcentaje de Missing Values'] 
st.table(tabla_info)
st.subheader('**Limpieza de los Datos**')

st.markdown(
    """
    #### **Missing Values:** 
    Para solucionar el problema de los missing values en las variables ph, sulfate y Trihalomethanes se \
    realizará una tabla con estadísticos descriptivos de estas y después se decidirá porque valor se remplazan los datos faltantes en la tabla. 
    """
)
st.table(df[['ph', 'Sulfate','Trihalomethanes']].describe())

st.write(""" Teniendo en cuenta los estadísticos descriptivos hallados en la tabla anterior vamos a reemplazar los datos faltantes de las tres \
    columnas por la mediana en cada uno de los casos, por cual utilizamos el siguiente código: 
""")

codigo1 = """ 
import pandas as pd 

df = pd.read_csv('https://raw.githubusercontent.com/labeconometria/MLxE/main/proyectos2do/datasets3.csv') # Importamos los datos
columnas = ['ph', 'Sulfate','Trihalomethanes']  # Creamos una lista con los nombres de las variables

# Rellenamos con las medianas los datos faltantes en las tres columnas
for columna in columnas:
    df[columna] = df[columna].fillna(df[columna].median())
"""

st.code(codigo1, language='python')

st.markdown(
    """
    #### **Datos Duplicados:** 
    En esta sección simplemente vamos a usar comandos de pandas para asegurarnos de que estamos eliminando cualquier registro duplicado de \
    la tabla datos, de ante mano se puede comentar que no se elimino ningun registro duplucado. El procedimiento lo haremos usando el siguiente código: 
    """
)

codigo2 = """
df.drop_duplicates(inplace=True)
"""
st.code(codigo2,language='python')
df = pd.read_csv('datos_transformados.csv')

st.subheader('**Categorización de Variables y Relación con Potability**')
st.write(
"""
En esta sección vamos a generar categorías dentro de cada una de las variables numérica generando intervalos, esto con el fin de crear tablas pívot para\
analizar la relación de estadístico como la media y la mediana en los grupos que se forman teniendo en cuenta el valor que toma la variable Potability. \
Para realizar este procedimiento se utiliza el siguiente código:
""")

codigo3 = """
columnas = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']

for columna in columnas:
  df['categorias_'+columna] = pd.cut(df[columna],bins=3)

for columna in columnas:
    pd.pivot_table(df,values=[columna],index='categorias_'+columna,columns='Potability',aggfunc=['mean','median'])
"""
st.code(codigo3,language='python')

columnas = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
for columna in columnas:
    st.markdown(f'##### Tabla Pivot Relacion Categorias {columna} y Potability')
    st.table(pd.pivot_table(df,values=[columna],index='categorias_'+columna,columns='Potability',aggfunc=['mean','median']))

st.write('''
Las tablas pívot generadas anteriormente nos podrán permitir realizar un primer acercamiento teórico a la identificación de si existen o no diferencias \
significativas entre la media y la mediana de los datos categorizadas por la variable objetivo, lo cual evidentemente surge a útil a la hora de plantar algún\
modelo de clasificación entre agua potable y no potable. Algunos aspectos interesantes a destacar de estas tablas es que también se generan categorías en la \
variable numérica por medio de la creación de intervalos, los cual permite realizar un análisis más profundo. 
''')

st.subheader("**Visualización**")
st.write("""
En esta sección se desarrollará una visualización de aspectos como la distribución, proporción y relación entre las variables de la tabla. En un primer\
 momento se puede observar histogramas sobre las distribuciones de las diferentes variables con el fin de analizar el comportamiento de estas. 
""")

st.image(image1)

st.write("""
Ahora se graficarán boxplots para analizar también la distribución de todas las variables, sin embargo, cada uno de estos será segmentado por la variable\
objetivo de esta tabla, “potabilty”, la cual hace referencia a si el agua es potable o no lo es. 
""")

st.image(image2)

st.write("""
Por último, visualizaremos un heatmap que nos indica el resultado de los índices de correlación calculados entre cada una de las variables de la tabla sin\
tener en cuenta las variables objetivo.
""")

st.image(image3)
st.write("""
El análisis de las graficas del los histogramas en conjunto con las de los boxplot nos permitirían realizar comentarios previos sobre el comportamiento que toma \
cada distribución, por ejemplo se podría identifica que algunas variables tienen valores donde se agrupa gran cantidad de datos entre otros aspectos a destacar, \
sin embargo en la sección final de conclusiones se hablara sobre el comportamiento de las distribuciones de las variable realizando un análisis conjunto entre la \
sección de las visualización y la de prueba de hipótesis que se presentara a continuación.  
""")

st.subheader("**Pruebas de Hipotesis**")
st.write("""
En esta sección buscaremos responder unas preguntas en especifico por medio del uso de pruebas de normalidad y pruebas de hipótesis, a continuación, se presentan\
 las preguntas y su respectivo desarrollo. 
""")

st.markdown("""
#### **¿El dataset sin la variable objetivo sigue una distribución normal multivariada?**\

Para analizar si el dataset sigue una distribución normal multivariada sin tener en cuenta la variable objetivo se va a realizar una prueba de normalidad, se puede usar \
el siguiente código y la ayuda del modulo pingouin para realizar este proceso (El nivel de significancia analizado sera del 5%) :

H_o : Las variables siguen una distribución normal multivariante.\

H_1 : Las variables NO siguen una distribución normal multivariante.

""")

codigo4 = """
import pingoin as pg 
df_ = df[['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
       'Organic_carbon', 'Trihalomethanes', 'Turbidity']]  # dataframe sin variable objetivo

pg.multivariate_normality(df_, alpha = .05 )

"""

st.code(codigo4,language='python')

st.table(pd.DataFrame({'HZ - Estadistico': {0: 1.336771641589833}, 'P-value': {0: 0.0}}).T)
st.write("""
Dado que el valor p de la prueba ES MENOR que nuestro valor alfa especificado de .05, rechazamos la hipótesis nula y aceptamos la alterna. Se puede suponer \
que el conjunto de datos NO sigue una distribución normal multivariante.
""")

st.markdown("""
#### **¿Cada una de las variables sigue una distribución normal?**


En esta sección se utilizará un test de shapiro para identificar si cada una de las variables por separado tienen o no una distribución normal, continuación\
se especificarán las hipótesis para esta prueba y así mismo el código con la que se puede realizar

Hipotesis:

H_0: La varible sigue una Distribución Normal

H_1: La variable no sigue una Distribución Normal

""")

codigo5 = """
estadisticos = []
p_values = []
variables = []
for columna in df_.columns:
  shapiro_test = stats.shapiro(df_[columna])
  variables.append(columna)
  estadisticos.append(shapiro_test[0])
  p_values.append(round(shapiro_test[1],5))

resultados = pd.DataFrame()
resultados['variable'] =variables
resultados['Estadistico'] = estadisticos
resultados['p-values'] = p_values

resultados

"""
st.code(codigo5,language='python')

st.table(pd.DataFrame({'variable': {0: 'ph',1: 'Hardness',2: 'Solids', 3: 'Chloramines',4: 'Sulfate',  5: 'Conductivity',6: 'Organic_carbon',
  7: 'Trihalomethanes',8: 'Turbidity'},'Estadistico': {0: 0.9797217845916748,1: 0.9959698915481567,2: 0.9777267575263977,3: 0.9967721700668335, 4: 0.9589976668357849,
  5: 0.9929699897766113,6: 0.9995209574699402,7: 0.9969625473022461,8: 0.9996957778930664},'p-values': {0: 0.0,1: 0.0,2: 0.0,3: 0.0,
  4: 0.0,5: 0.0,6: 0.62022,7: 0.0,8: 0.93069}}))

st.write("""

Se puede observar por el nivel del p- valor en contraste con el nivel de significancia fijado en un 5%, que las únicas variables para las cuales se puede aceptar \
la hipótesis nula y por ende comentar que se compartan como una distribución normal son Organic_carbon y Turbidity . Para el resto de variables se tiene que rechazar\
 la hipótesis nula y por ende comentar que no siguen una distribución normal.

""")

st.markdown("""
#### **¿Existe alguna diferencia en la media de cada una de las variables si se divide el dataset en agua potable y no potable?**


A continuación, se van a realizar pruebas Z con el fin de identificar si es significativa o no la diferencia entre medias por variable siendo segregadas en agua potable \
(1) y la que no es potable (0). Se mostrarán la hipótesis manejada y el código usado para determinar tanto el estadístico como el p valor (recordar que se está trabajando\
 con un nivel de confianza del 5%)

Hipotesis:

H_0 : La diferencia entre medias no es significativa 

H_1: La diferencia ente medias es significativa 

""")

codigo6 = """
for columna in df_.columns:
  info = pd.pivot_table(data=df,index='Potability',values=columna,aggfunc=['mean',np.var,'count'])
  st.markdown(f"#### **Variable: {columna}**")
  st.table(info)
  media1 = info['mean'][columna][1]
  media2 = info['mean'][columna][0]

  var1 = info['var'][columna][1]
  var2 = info['var'][columna][0]

  n1 = info['count'][columna][1]
  n2 = info['count'][columna][0]

  Z = (media1 - media2)/((var1/n1)+(var2/n2))**(1/2)
  pvalue = 2 * stats.norm.sf(abs(Z))

"""
st.code(codigo6,language='python')

lista = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
       'Organic_carbon', 'Trihalomethanes', 'Turbidity']

for columna in lista:
  info = pd.pivot_table(data=df,index='Potability',values=columna,aggfunc=['mean',np.var,'count'])
  st.markdown(f"#### **Variable: {columna}**")
  st.table(info)
  media1 = info['mean'][columna][1]
  media2 = info['mean'][columna][0]

  var1 = info['var'][columna][1]
  var2 = info['var'][columna][0]

  n1 = info['count'][columna][1]
  n2 = info['count'][columna][0]

  Z = (media1 - media2)/((var1/n1)+(var2/n2))**(1/2)
  pvalue = 2 * stats.norm.sf(abs(Z))
  
  st.markdown(f""" 
  ###### **Resultados Prueba**

  Estadistico Z = {Z}

  P-valor = {pvalue}
  """)

  if pvalue>0.05:
    st.markdown(f'**Conclusión:** Se acepta la hipotesis nula, la diferencia entre medias de la varible {columna} segregada por la variable Potability no es significativa.')
  else:
    st.markdown(f'**Conclusión:** Se acepta la hipotesis nula, la diferencia entre medias de la varible {columna} segregada por la varaible Potability es significativa.')


st.markdown("""
## **Concluciones** 


Este dataset sobre variables que asociadas a la calidad del agua permitió realizar ciertos análisis tanto de visualización como estadísticos, de los cuales podemos destacar algunos\
 aspectos como los siguientes:

-	Para la mayoría de variables, al generar intervalos para de cierta manera mostrar categorías (lo realizado en las tabla pivot), se puede identificar que a priori en la mayoría de los \
  casos los estadísticos descriptivos de la media y mediana al agregar la segmentación adicional sujeto a la variable Potability, no diferían mucho en magnitud, lo cual nos podría dar ciertos\
 indicios sobre los resultados de las pruebas de hipótesis realizadas en la última sección sobre la media de las variables categorizada por la variable objetivo.

-	Al realizar un análisis grafico de los coeficientes de relación entre las variables, se puede concluir que ninguna de las relaciones entre las variables es de magnitud alta, el total de estas\
 esta por debajo de 0.4 y muy cercano a 0.

- Al momento de realizar la visualización de los histogramas no se podría establecer con certeza cuál de las variables se comportaría siguiendo una distribución normal, además en algunas de estas \
se podía identificar algunos sesgos en el comportamiento de los datos entre otros aspectos, sin embargo, al realizar las pruebas de hipótesis correspondiente se puede evidenciar tanto estadísticamente\
  como gráficamente que las variable que se comportan bajo una distribución normal son  Organic_carbon y Turbidity.
 

""")