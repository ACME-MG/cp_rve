from modules.api import API
api = API("", 0)
api.add_input("500/16_s1_vs_czm.csv")
api.add_input("500/16_s2_vs_czm.csv")
api.plot_curves(directions="x")