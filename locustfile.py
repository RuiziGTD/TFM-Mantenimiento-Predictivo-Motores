from locust import HttpUser, task, between

# El mismo CSV dummy de antes
CSV_DATA = """unit_number,time_in_cycles,op_setting_1,op_setting_2,op_setting_3,T2,T24,T30,T50,P2,P15,P30,Nf,Nc,epr,Ps30,phi,NRf,NRc,BPR,farB,htBleed,Nf_dmd,PCNfR_dmd,W31,W32
1,1,-0.0007,-0.0004,100.0,518.67,641.82,1589.70,1400.60,14.62,21.61,554.36,2388.06,9046.19,1.30,47.47,521.66,2388.02,8138.62,8.4195,0.03,392,2388,100.0,39.06,23.4190"""

class UsuarioCarga(HttpUser):
    wait_time = between(1, 2)

    @task
    def enviar_csv(self):
        # Preparamos el archivo para subir
        files = {
            'file': ('sensor_dump.csv', CSV_DATA, 'text/csv')
        }
        # Locust hace el POST multipart
        self.client.post("/predict", files=files)