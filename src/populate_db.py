from setup import *
import pandas as pd
import json
import csv
import math

def populate_with_users(conn, users_df):
    with conn.cursor() as cursor:
        print("Gonna insert", len(users_df['account_no'].unique()), "users")
        for line, account_no in enumerate(users_df['account_no'].unique()):
            cursor.execute("""
                INSERT IGNORE INTO users (username, name)
                VALUES (%s, "Default Name")
                """,
                (account_no)
            )
            print(line)


def populate_with_bundles(conn, recipes_path):
    try:
        with open(recipes_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        recipes = data.get("recipes", [])
        print(f"\nCarregando {len(recipes)} receitas do JSON...\n")

        with conn.cursor() as cur:
            for bundle_id, recipe in enumerate(recipes, start=1):
                name = recipe["name"]
                description = recipe["description"]
                image_url = recipe["image_url"]
                instructions = "\n".join(recipe["instructions"])

                cur.execute("""
                    INSERT IGNORE INTO bundles (bundle_id, name, description, instructions, image_url)
                    VALUES (%s, %s, %s, %s, %s)
                """, (bundle_id, name, description, instructions, image_url))

                for ingr_id, ingredient in enumerate(recipe["ingredients"]):
                    product = ingredient["product"]
                    quantity = math.ceil(ingredient["quantity"])

                    # Inserir relação na tabela `bundle_items`
                    cur.execute("""
                        INSERT IGNORE INTO bundle_items (bundle_id, ingredient, quantity)
                        VALUES (%s, %s, %s)
                    """, (bundle_id, product, quantity))


        # FIXME: Im pretty sure this is not needed since the 'raii-like' python with statement does this commit when out of scope
        # only remove/test this when theres time
        conn.commit()
        print("✅ Base de dados populada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao popular a base de dados: {e}")


def populate_with_items(conn, items_path):
    try:                
        df = pd.read_csv(items_path, sep=';', encoding='utf-8')

        selected_columns = ["sku", "product_dsc", df.columns[-1]]  
        df = df[selected_columns]

        df.columns = ["item_id", "name", "price_index"]

        df["image_url"] = None  

        print(df.head())

        with conn.cursor() as cur:
            num_items = len(df.index)
            for index, row in df.iterrows():
                cur.execute("""
                    INSERT IGNORE INTO items (item_id, name, image_url, price_index) 
                    VALUES (%s, %s, %s, %s)
                """, (row["item_id"], row["name"], row["image_url"], row["price_index"]))
                print(f'populating items {index} / {num_items}')

        conn.commit()
        print("✅ Base de dados populada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao popular a base de dados: {e}")




if __name__ == '__main__':
    conn = connect_db()
    setup_db(conn, cleanup=True)

    sales_df = pd.read_csv("../datasets/sample_sales_info_encripted.csv", sep=",", quotechar='"', encoding="utf-8", on_bad_lines="skip")
    items_df = pd.read_csv("../datasets/sample_prod_info.csv", sep=",", quotechar='"', encoding="utf-8", on_bad_lines="skip")
    
    items_path = "../datasets/sample_prod_info.csv"

    # Populate with users
    print("Populating database with users")
    #populate_with_users(conn, sales_df)
    
    # Populate with bundles and blunde items
    print("Populating database with bundles")
    populate_with_bundles(conn, "../recipes.json")

    # Populate with items
    print("Populating database with items data")
    populate_with_items(conn, items_path)

    conn.close()
