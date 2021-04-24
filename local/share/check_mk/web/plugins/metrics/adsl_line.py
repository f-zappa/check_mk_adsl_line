from cmk.gui.i18n import _
#from cmk.gui.plugins.metrics import metric_info

check_metrics["check_mk-adsl_line"] = {
        "adsl_down_rate": { "name" : "adsl_down_rate" },
        "adsl_up_rate": { "name" : "adsl_up_rate" },
        "adsl_attainable": { "name" : "adsl_attainable" },
        "adsl_snr_margin": { "name" : "adsl_snr_margin" },
        "adsl_attenuation": { "name" : "adsl_attenuation" },
        "adsl_output_power": { "name" : "output_signal_power_dbm" },
   }

metric_info["adsl_down_rate"] = {
         "title": _("Downstream Rate"),
         "unit": "bits/s",
         "color": "33/a",
   }

metric_info["adsl_up_rate"] = {
         "title": _("Upstream Rate"),
         "unit": "bits/s",
         "color": "12/a",
   }

metric_info["adsl_attainable"] = {
         "title": _("Attainable Rate"),
         "unit": "bits/s",
         "color": "41/b",
         "auto_graph": False,
   }

metric_info["adsl_attenuation"] = {
         "title": _("Signal Attenuation"),
         "unit": "db",
         "color": "43/b",
   }

metric_info["adsl_snr_margin"] = {
         "title": _("SNR Margin"),
         "unit": "db",
         "color": "45/b",
   }

graph_info["adsl_down_rate"] = {
            "metrics": [("adsl_down_rate", "area"),
                        ("adsl_attainable","line")],
            "scalars": [
                         "adsl_down_rate:warn",
                         "adsl_down_rate:crit", ],
    }

graph_info["adsl_up_rate"] = {
            "metrics": ("adsl_up_rate", "area"),
            "scalars": [
                         "adsl_up_rate:warn",
                         "adsl_up_rate:crit", ],
    }

graph_info["adsl_snr_margin"] = {
            "metrics": ("adsl_snr_margin", "area"),
            "scalars": [
                         "adsl_snr_margin:warn",
                         "adsl_snr_margin:crit", ],
    }

graph_info["adsl_attenuation"] = {
            "metrics": ("adsl_attenuation", "area"),
            "scalars": [
                         "adsl_attenuation:warn",
                         "adsl_attenuation:crit", ],
    }

