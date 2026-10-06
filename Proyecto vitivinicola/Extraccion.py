import pandas as pd
import numpy as np  
import json
#FUNCIONES---
def Inferir_variedad(fila):
    if pd.notna(fila['variedad']) and str(fila['variedad']).lower() != 'nan':
        return str(fila['variedad']).title()

    producto = str(fila['producto']).strip().lower()
    color = str(fila['color']).strip().lower()

    if 'varietal' in producto:
        if 'tinto' in color or 'tinto' in producto:
            return 'Malbec'
        elif 'blanco' in color or 'blanco' in producto:
            return 'Chardonnay'
        elif 'rosado' in color or 'rosado' in producto:
            return 'Malbec Rosé'

    if 'espumoso' in producto or 'espumante' in producto or 'frizzante' in producto:
        return 'Blend Espumante'

    if 'tinto' in color or 'tinto' in producto:
        if 'dulce' in producto or 'endulzado' in producto:
            return 'Blend Tinto Dulce'
        else:
            return 'Blend Tinto'
            
    elif 'blanco' in color or 'blanco' in producto:
        if 'dulce' in producto or 'endulzado' in producto:
            return 'Blend Blanco Dulce'
        else:
            return 'Blend Blanco'
            
    elif 'rosado' in color or 'rosado' in producto:
        if 'dulce' in producto or 'endulzado' in producto:
            return 'Blend Rosado Dulce'
        else:
            return 'Blend Rosado'

    return 'Varietal No Especificado'

def categorizar_estilo(prod):
    prod_lower = str(prod).lower()
    if 'organico' in prod_lower:
        return 'Orgánico Certificado'
    elif 'reserva' in prod_lower:
        return 'Reserva'
    elif 'varietal' in prod_lower:
        return 'Varietal Estándar'
    else:
        return 'Genérico / Mesa'
#-----------------------------------------------------------------------------------

exportaciones = pd.read_csv("inv-exportanciones-2025-ene-abr.csv",  encoding='latin1')

#---limpieza -------
exportaciones = exportaciones[exportaciones['producto'].str.contains('Vino', case=False, na=False)]
valores_a_reemplazar = ['sin variedad', 'nan', '', 'none', 'sin_variedad']

for col in ['variedad_1', 'variedad_2', 'variedad_3']:
    exportaciones[col] = exportaciones[col].str.lower().str.strip()
    exportaciones.loc[exportaciones[col].isin(valores_a_reemplazar), col] = np.nan

exportaciones['variedad_1'] = exportaciones['variedad_1'].fillna(exportaciones['variedad_2']).fillna(exportaciones['variedad_3'])

exportaciones = exportaciones.drop(columns=['variedad_2', 'variedad_3'])
exportaciones= exportaciones.rename(columns={'variedad_1': 'variedad'})
exportaciones['variedad'] = exportaciones.apply(Inferir_variedad, axis=1)

exportaciones = exportaciones.drop(columns=['hl_exportados'], errors='ignore')
exportaciones = exportaciones.drop(columns=['valor_fob_litros'], errors='ignore')
#---------------

exportaciones.to_excel('Exportaciones2025.xlsx', index=False)

#TRATAMIENTO PARA METRICAS-----------------------------
comercial = exportaciones[exportaciones['valor_fob_miles'] > 0].copy()
comercial['precio_por_litro'] = (comercial['valor_fob_miles'] * 1000) / comercial['litros_exportados']
comercial['estilo_vino'] = comercial['producto'].apply(categorizar_estilo)

organicos = exportaciones[exportaciones['producto'].str.contains('organico', case=False, na=False)].copy()
organicos_comerciales = organicos[organicos['valor_fob_miles'] > 0].copy()
organicos_comerciales['fob_usd'] = organicos_comerciales['valor_fob_miles'] * 1000
#-----------------------------------------------

# =====================================================================
# 📈 DEMOSTRACIÓN 1: El precio por litro según el valor agregado
# =====================================================================
evidencia_estilos = comercial.groupby('estilo_vino').agg(
    litros_totales=('litros_exportados', 'sum'),
    fob_totales_usd=('valor_fob_miles', lambda x: x.sum() * 1000)
).reset_index()

evidencia_estilos['precio_promedio_litro'] = (
    evidencia_estilos['fob_totales_usd'] / evidencia_estilos['litros_totales']
)

total_litros = evidencia_estilos['litros_totales'].sum()
total_fob = evidencia_estilos['fob_totales_usd'].sum()
evidencia_estilos['%_volumen'] = (evidencia_estilos['litros_totales'] / total_litros) * 100
evidencia_estilos['%_valor'] = (evidencia_estilos['fob_totales_usd'] / total_fob) * 100

evidencia_estilos = evidencia_estilos.sort_values(by='precio_promedio_litro', ascending=False).reset_index(drop=True)

# =====================================================================
# 📈 DEMOSTRACIÓN 2: El riesgo logístico del Granel vs Fraccionado (PONDERADO)
# =====================================================================
evidencia_logistica = comercial.groupby('modalidad_envio').agg(
    litros_totales=('litros_exportados', 'sum'),
    fob_totales_usd=('valor_fob_miles', lambda x: x.sum() * 1000)
).reset_index()

evidencia_logistica['precio_promedio_litro'] = (
    evidencia_logistica['fob_totales_usd'] / evidencia_logistica['litros_totales']
)

# =====================================================================
# 📈 DEMOSTRACIÓN 3: Foco Geográfico (Países que mejor pagan el vino Orgánico)
# =====================================================================
df_org = comercial[comercial['estilo_vino'] == 'Orgánico Certificado']
df_org['precio_operacion_litro'] = (df_org['valor_fob_miles'] * 1000) / df_org['litros_exportados']

evidencia_paises_org = df_org.groupby('pais').agg(
    litros_totales=('litros_exportados', 'sum'),
    precio_mediano=('precio_operacion_litro', 'median'),      # Métrica robusta central
    techo_precio_p75=('precio_operacion_litro', lambda x: x.quantile(0.75)), # El top 25% más caro
    cantidad_embarques=('litros_exportados', 'count')
).reset_index()


evidencia_paises_org = evidencia_paises_org[evidencia_paises_org['litros_totales'] > 500]

# Ordenamos por el PRECIO MEDIANO ROBUSTO
ranking_robusto = evidencia_paises_org.sort_values(by='precio_mediano', ascending=False).reset_index(drop=True)

# =====================================================================
# 🗺️ GEOGRAFÍA DE LA SUSTENTABILIDAD: Ranking por provincia de origen orgánico
# =====================================================================
reporte_provincias_organicas = organicos_comerciales.groupby('provincia_depositario').agg(
    litros_totales=('litros_exportados', 'sum'),
    fob_totales_usd=('fob_usd', 'sum')
).reset_index()

reporte_provincias_organicas['precio_promedio_litro'] = (
    reporte_provincias_organicas['fob_totales_usd'] / reporte_provincias_organicas['litros_totales']
)

total_litros_org = reporte_provincias_organicas['litros_totales'].sum()
reporte_provincias_organicas['%_participacion_volumen'] = (
    reporte_provincias_organicas['litros_totales'] / total_litros_org
) * 100

reporte_provincias_organicas = reporte_provincias_organicas.sort_values(by='litros_totales', ascending=False).reset_index(drop=True)

#Prints ----------------------------------------
print("📊 EVIDENCIA 1: VALOR AGREGADO VS COMODITIZACIÓN")
print(evidencia_estilos.to_string(index=False))
print("\n📦 EVIDENCIA 2: IMPACTO DE LA MODALIDAD DE ENVÍO EN EL PRECIO")
print(evidencia_logistica[['modalidad_envio', 'litros_totales', 'precio_promedio_litro']].to_string(index=False))
print("\n🌍 EVIDENCIA 3: FOCO GEOGRÁFICO PARA EL SEGMENTO ORGÁNICO")
print(ranking_robusto.head(10).to_string(index=False))
print("🌍 RANKING GEOGRÁFICO EXCLUSIVO DE VINOS ORGÁNICOS EXPORTADOS (Ene-Abr 2025):")
print(reporte_provincias_organicas.to_string(index=False))



pd.options.display.float_format = '{:,.2f}'.format

#CONVERTIR EN JSON 
columnas_web = [
    'pais', 'producto', 'color', 'modalidad_envio', 
    'provincia_depositario', 'litros_exportados', 
    'valor_fob_miles', 'variedad', 'estilo_vino', 'precio_por_litro'
]

paquete_datos_totales = {
    "ranking_paises": ranking_robusto.to_dict(orient='records'),
    "ranking_provincias": reporte_provincias_organicas.to_dict(orient='records'),
    "registros_totales": comercial[columnas_web].to_dict(orient='records') 
}

with open('datos_completos.json', 'w', encoding='utf-8') as f:
    json.dump(paquete_datos_totales, f, ensure_ascii=False, indent=4)

print("\n🚀 ¡ÉXITO ABSOLUTO! Se generó 'datos_completos.json' ")
