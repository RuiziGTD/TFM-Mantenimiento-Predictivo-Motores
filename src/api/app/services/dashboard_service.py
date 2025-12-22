import numpy as np

class DashboardService:

    @staticmethod
    def build_health_view(units, predictions):
        """
        Vista 1: Estado de salud de los motores
        """

        predictions = np.array(predictions)

        # Clasificación
        status = []
        for rul in predictions:
            if rul < 30:
                status.append("CRITICO")
            elif rul < 80:
                status.append("AVISO")
            else:
                status.append("OK")

        units_status = [
            {
                "unit_id": int(units[i]),
                "rul": float(predictions[i]),
                "status": status[i]
            }
            for i in range(len(predictions))
        ]

        overview = {
            "total_units": len(predictions),
            "rul_min": float(predictions.min()),
            "rul_mean": float(predictions.mean()),
            "rul_max": float(predictions.max()),
            "critical_units": status.count("CRITICO"),
            "warning_units": status.count("AVISO"),
            "ok_units": status.count("OK")
        }

        return {
            "overview": overview,
            "units": units_status
        }
