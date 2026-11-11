"""One color per item, shared by every figure.

Rules (Plante & Cushman 2020, Res Pract Thromb Haemost, PMC7040535): use the
same palette in all figures, give an item the same color everywhere, separate
colors by lightness, use shades of one hue for related items. Hues are
ColorBrewer palettes (Blues, Purples, Oranges, BrBG teals, Reds, Greys). Orange (semi-public)
and teal (public) stay distinct for red-green colour-blind readers.
"""

COLORS = {
    # A: battery EV subsidy (Blues)
    "A_all": "#08519c",
    "A_city": "#6baed6",
    # B: FCEV subsidy (Purples)
    "B_all": "#756bb1",
    "B_city": "#cbc9e2",
    # semi-public operation (Oranges): C, R under 준공영제, city bus money
    "C": "#e6550d",
    "R_C": "#fdae6b",
    # public operation (teals, BrBG): D, R under a public operator, T2
    "D": "#003c30",
    "R_D": "#35978f",
    "T2": "#01665e",
    # E: fare pass (yellow, close to RPTH accent yellow)
    "E": "#ffd92f",
    # hydrogen tram by pathway (Reds, darker = more CO2)
    "H2_smr": "#67000d",
    "H2_mix": "#cb181d",
    "H2_biogas": "#fb6a4a",
    "H2_green": "#fee0d2",
    # electric options (blues; lighter than the EV subsidy blue)
    "tram_battery": "#3182bd",
    "bus_electric": "#9ecae1",
    # W: tram construction congestion (dark grey-brown, distinct from car grey)
    "W": "#7f4f24",
    # 특구1 campus loop bus
    "tukgu": "#c51b7d",
    # reference modes (Greys)
    "bus_cng": "#a8a8a8",
    "car": "#525252",
    # totals
    "operating_cost": "#252525",
}

# waterfall: savings in light teals (public side), new costs in reds
WATERFALL = {
    "Semi-public standard cost": COLORS["C"],
    "Guaranteed profit + bonus": "#80cdc1",
    "Duplicated executives/admin": "#c7eae5",
    "Leakage (overpayment, fraud)": "#e8f6f3",
    "Pay change per driver vs today": "#fcbba1",
    "Public-operator efficiency": "#fc9272",
    "Route-licence buyout": "#ef3b2c",
    "Depots (net of rent)": "#cb181d",
    "Transition cost": "#99000d",
    "Public operator unit cost": COLORS["D"],
}

# tornado: parameter at low / high value (RdBu ends, different lightness)
TORNADO_LOW = "#92c5de"
TORNADO_HIGH = "#b2182b"
