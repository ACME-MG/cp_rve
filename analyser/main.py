from modules.api import API
api = API("", 0)
api.add_input("500/16_s1.csv")
api.add_input("500/16_s2.csv")
api.add_input("500/32_s1.csv")
api.plot_curves(directions="x")