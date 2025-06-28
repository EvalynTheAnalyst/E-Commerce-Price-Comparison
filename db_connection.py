from web_scraping import matched
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os 
import pandas as pd
import sqlalchemy

def save_to_data():
    load_dotenv()
    
    host = os.getenv('host')
    database = os.getenv('database')
    username = os.getenv('username')
    port = os.getenv('port')
    password = os.getenv('password')

    
    engine = create_engine(f'postgresql+psycopg2://eva:1234@{host}:{port}/{database}')


    with engine.connect() as conn:
            print("Connection successful")
    
    
    
    print("DataFrame created with", len(matched), "rows")

    print("Engine type:", type(engine))
    print("Engine repr:", repr(engine))
    print("SQLAlchemy version:", sqlalchemy.__version__)
    print("Pandas version:", pd.__version__)
     
    try:
        matched.to_sql('price_comparison', 
                    con = engine, 
                    schema='jumia_data',
                    if_exists='replace',
                    index = False, 
                    method='multi')
        
    
        print("Data inserted successfully.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
   save_to_data()