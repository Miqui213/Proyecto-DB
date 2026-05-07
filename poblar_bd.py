import pandas as pd
from sqlalchemy import create_engine
import pymongo
import json
import sys

# Configuración de red (Localhost porque correrá dentro de la EC2 de BD)
HOST = '127.0.0.1'

# ==========================================
# 1. POSTGRESQL (Microservicio de Tickets)
# ==========================================
print("Conectando a PostgreSQL...")
# Reemplaza 'TU_PASSWORD_AQUI' por la clave que pusiste en CloudFormation
try:
    engine_pg = create_engine(f'postgresql://u_tickets:TU_PASSWORD_AQUI@{HOST}:5432/travel_tickets')
    
    print("   -> Cargando destinos...")
    df_destinos = pd.read_csv('destinos.csv')
    df_destinos.to_sql('destinos', engine_pg, if_exists='append', index=False)
    
    print("   -> Cargando vuelos...")
    df_vuelos = pd.read_csv('vuelos.csv')
    df_vuelos.to_sql('vuelos', engine_pg, if_exists='append', index=False)
    print("PostgreSQL poblado con éxito.\n")
except Exception as e:
    print(f"Error en PostgreSQL: {e}\n")

# ==========================================
# 2. MYSQL (Microservicio de Usuarios)
# ==========================================
print("Conectando a MySQL...")
try:
    # Usamos la contraseña que configuraste en tu comando manual de Docker
    engine_mysql = create_engine(f'mysql+pymysql://u_usuarios:UsuariosAdmin2026!@{HOST}:3306/db_usuarios')
    
    print("   -> Cargando 20,000 usuarios...")
    df_usuarios = pd.read_csv('usuarios_20000.csv')
    df_usuarios.to_sql('usuarios', engine_mysql, if_exists='append', index=False)
    print("✅ MySQL poblado con éxito.\n")
except Exception as e:
    print(f"Error en MySQL: {e}\n")

# ==========================================
# 3. MONGODB (Microservicio de Reservas)
# ==========================================
print("🛒 Conectando a MongoDB...")
try:
    client = pymongo.MongoClient(f"mongodb://{HOST}:27017/")
    db_mongo = client["reservas_db"]
    coleccion = db_mongo["reservas"]
    
    print("   -> Cargando 20,000 reservas...")
    with open('reservas.json', 'r', encoding='utf-8') as f:
        data_reservas = json.load(f)
        
    # Limpiamos la colección por si corres el script dos veces
    coleccion.delete_many({}) 
    coleccion.insert_many(data_reservas)
    
    print("MongoDB poblado con éxito.\n")
except Exception as e:
    print(f"Error en MongoDB: {e}\n")

print("🎉 ¡TODAS LAS BASES DE DATOS ESTÁN LISTAS Y CARGADAS! 🎉")