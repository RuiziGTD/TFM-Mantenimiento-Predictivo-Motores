import requests
import io

# URL de la API
URL = "http://localhost:8000/predict"

# Simulamos el contenido de un CSV
csv_content = """unit_number,time_in_cycles,op_setting_1,op_setting_2,op_setting_3,T2,T24,T30,T50,P2,P15,P30,Nf,Nc,epr,Ps30,phi,NRf,NRc,BPR,farB,htBleed,Nf_dmd,PCNfR_dmd,W31,W32
1,1,-0.0007,-0.0004,100.0,518.67,641.82,1589.70,1400.60,14.62,21.61,554.36,2388.06,9046.19,1.30,47.47,521.66,2388.02,8138.62,8.4195,0.03,392,2388,100.0,39.06,23.4190"""

def test_upload_csv():
    print(f"🔵 Conectando a {URL} enviando CSV...")
    
    # Creamos un archivo en memoria
    archivo_falso = {'file': ('test_sensor.csv', csv_content, 'text/csv')}

    try:
        response = requests.post(URL, files=archivo_falso)
        
        if response.status_code == 200:
            print("✅ ÉXITO (200 OK)")
            print(f"Respuesta: {response.json()}")
        else:
            print(f"❌ FALLO ({response.status_code})")
            print(response.text)

    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_upload_csv()