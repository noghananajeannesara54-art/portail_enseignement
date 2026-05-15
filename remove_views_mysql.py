#!/usr/bin/env python
"""
Supprimer les vues invalides MySQL
"""

import mysql.connector

def remove_invalid_views():
    """Supprimer uniquement les vues invalides"""
    
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='portail_enseignement',
            port=3306
        )
        
        cursor = conn.cursor()
        
        print("=== SUPPRESSION VUES INVALIDES ===")
        
        # Lister toutes les vues
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        
        print(f"\n📊 Vues trouvées: {len(views)}")
        
        if views:
            print("\n🗑️ Suppression des vues:")
            for view in views:
                view_name = view[0]
                try:
                    cursor.execute(f"DROP VIEW IF EXISTS `{view_name}`")
                    print(f"   ✅ {view_name} supprimée")
                except Exception as e:
                    print(f"   ❌ Erreur {view_name}: {e}")
        
        # Vérification finale
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n📊 Tables finales: {len(tables)}")
        print("\n📋 Liste finale:")
        
        for table in tables:
            table_name = table[0]
            try:
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table_name}: {count} enregistrements")
            except Exception as e:
                print(f"   ⚠️ {table_name}: Vue ou erreur - {e}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Nettoyage terminé!")
        
    except mysql.connector.Error as e:
        print(f"❌ Erreur MySQL: {e}")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

if __name__ == '__main__':
    remove_invalid_views()
