#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 November 27
#
# This code contains the function used to calculate the M and V coefficients for spell base damage.
#


from numba import njit

@njit
def get_mv(tier, player_int, enemy_int):
    #
    # Determine the M and V values to use based on dINT and ninjutsu skill
    #
    # The M and V values were determined through my testing, which I present in this thread:
    # https://www.ffxiah.com/forum/topic/56749/updated-ninjutsu-damage-formulae
    #
    dINT = player_int - enemy_int

    if tier=="Ichi":
        if dINT <= -9:
            m=0.00; v=11.0
        elif dINT <= -1:
            m=0.50; v=16.0
        elif dINT <= 24:
            m=1.00; v=16.0
        elif dINT <= 74:
            m=0.50; v=28.5
        else:
            m=0.00; v=66.0

    elif tier=="Ni":
        if dINT <= -43:
            m=0.00; v=47.0
        elif dINT <= -1:
            m=0.50; v=69.0
        elif dINT <= 112:
            m=1.00; v=69.0
        elif dINT <= 338:
            m=0.50; v=125.5
        else:
            m=0.00; v=295.0

    elif tier=="San":
        if dINT <= -53:
            m=0.00; v=81.0
        elif dINT <= 1:
            m=1.00; v=134.0
        elif dINT <= 353:
            m=1.50; v=134.0
        else:
            m=0.00; v=655.0

    return(m,v)
    
def get_mv_blm(element, tier, player_int, enemy_int):
    #
    # Using the table from BG wiki
    #

    # The table on BG wiki does not list negative dINT values.
    # Ninjutsu clearly shows different slopes for negative dINT.
    # I'm currently assuming that the lower dINT limit is 0, such that any negative dINT is converted to 0.
    # This does not appear to be the case on preliminary testing, but it's better than what I was using previously.
    # BG states 
    #     "With a negative dINT, calculated value for D will be lower than V, potentially even 0."
    #   which is not very helpful.

    dINT = player_int - enemy_int
    if dINT < 50:
        window = "0"
    elif dINT < 100:
        window = "50"
    elif dINT < 200:
        window = "100"
    elif dINT < 300:
        window = "200"
    elif dINT < 400:
        window = "300"
    elif dINT < 500:
        window = "400"
    elif dINT < 600:
        window = "500"
    else:
        window = "600"

    # print(element, tier, window)
    mv = {
    "I":{"earth":  {"0":[10,2.0],"50":[110,1.0],"100":[160,0],"200":[160,0],"300":[160,0],"400":[160,0],"500":[160,0],"600":[160,0]},
         "water":  {"0":[25,1.8],"50":[115,1.0],"100":[165,0],"200":[165,0],"300":[165,0],"400":[165,0],"500":[165,0],"600":[165,0]},
         "wind":   {"0":[40,1.6],"50":[120,1.0],"100":[170,0],"200":[170,0],"300":[170,0],"400":[170,0],"500":[170,0],"600":[170,0]},
         "fire":   {"0":[55,1.4],"50":[125,1.0],"100":[175,0],"200":[175,0],"300":[175,0],"400":[175,0],"500":[175,0],"600":[175,0]},
         "ice":    {"0":[70,1.2],"50":[130,1.0],"100":[180,0],"200":[180,0],"300":[180,0],"400":[180,0],"500":[180,0],"600":[180,0]},
         "thunder":{"0":[85,1.0],"50":[135,1.0],"100":[185,0],"200":[185,0],"300":[185,0],"400":[185,0],"500":[185,0],"600":[185,0]}},
    "II":{"earth":  {"0":[100,3.0],"50":[250,2.0],"100":[350,1],"200":[450,0],"300":[450,0],"400":[450,0],"500":[450,0],"600":[450,0]},
         "water":   {"0":[120,2.8],"50":[260,1.9],"100":[355,1],"200":[455,0],"300":[455,0],"400":[455,0],"500":[455,0],"600":[455,0]},
         "wind":    {"0":[140,2.6],"50":[270,1.8],"100":[360,1],"200":[460,0],"300":[460,0],"400":[460,0],"500":[460,0],"600":[460,0]},
         "fire":    {"0":[160,2.4],"50":[280,1.7],"100":[365,1],"200":[465,0],"300":[465,0],"400":[465,0],"500":[465,0],"600":[465,0]},
         "ice":     {"0":[180,2.2],"50":[290,1.6],"100":[370,1],"200":[470,0],"300":[470,0],"400":[470,0],"500":[470,0],"600":[470,0]},
         "thunder": {"0":[200,2.0],"50":[300,1.5],"100":[375,1],"200":[475,0],"300":[475,0],"400":[475,0],"500":[475,0],"600":[475,0]}},
    "III":{"earth":  {"0":[200,4.0],"50":[400,3.0],"100":[550,2.00],"200":[750,1.0],"300":[850,0],"400":[850,0],"500":[850,0],"600":[850,0]},
         "water":    {"0":[230,3.7],"50":[415,2.9],"100":[560,1.95],"200":[755,1.0],"300":[855,0],"400":[855,0],"500":[855,0],"600":[855,0]},
         "wind":     {"0":[260,3.4],"50":[430,2.8],"100":[570,1.90],"200":[760,1.0],"300":[860,0],"400":[860,0],"500":[860,0],"600":[860,0]},
         "fire":     {"0":[290,3.1],"50":[445,2.7],"100":[580,1.85],"200":[765,1.0],"300":[865,0],"400":[865,0],"500":[865,0],"600":[865,0]},
         "ice":      {"0":[320,2.8],"50":[460,2.6],"100":[590,1.80],"200":[770,1.0],"300":[870,0],"400":[870,0],"500":[870,0],"600":[870,0]},
         "thunder":  {"0":[350,2.5],"50":[475,2.5],"100":[600,1.75],"200":[775,1.0],"300":[875,0],"400":[875,0],"500":[875,0],"600":[875,0]}},
    "IV":{"earth":  {"0":[400,5.0],"50":[650,4.0],"100":[850,3.00],"200":[1150,2.00],"300":[1350,1.0],"400":[1450,0],"500":[1450,0],"600":[1450,0]},
         "water":   {"0":[440,4.7],"50":[675,3.9],"100":[870,2.95],"200":[1165,1.99],"300":[1364,1.0],"400":[1464,0],"500":[1464,0],"600":[1464,0]},
         "wind":    {"0":[480,4.4],"50":[700,3.8],"100":[890,2.90],"200":[1180,1.98],"300":[1378,1.0],"400":[1478,0],"500":[1478,0],"600":[1478,0]},
         "fire":    {"0":[520,4.1],"50":[730,3.7],"100":[915,2.85],"200":[1195,1.97],"300":[1397,1.0],"400":[1497,0],"500":[1497,0],"600":[1497,0]},
         "ice":     {"0":[560,4.8],"50":[755,3.6],"100":[935,2.80],"200":[1210,1.96],"300":[1411,1.0],"400":[1511,0],"500":[1511,0],"600":[1511,0]},
         "thunder": {"0":[600,4.5],"50":[780,3.5],"100":[955,2.75],"200":[1225,1.95],"300":[1325,1.0],"400":[1525,0],"500":[1525,0],"600":[1525,0]}},
    "V":{"earth":  {"0":[650,6.0],"50":[ 950,5.00],"100":[1200,4.00],"200":[1600,3.00],"300":[1900,2.00],"400":[2100,1.0],"500":[2200,0],"600":[2200,0]},
         "water":  {"0":[700,5.6],"50":[ 980,4.74],"100":[1217,3.95],"200":[1612,2.99],"300":[1911,1.99],"400":[2110,1.0],"500":[2210,0],"600":[2210,0]},
         "wind":   {"0":[750,5.2],"50":[1110,4.50],"100":[1235,3.90],"200":[1625,2.98],"300":[1923,1.98],"400":[2121,1.0],"500":[2221,0],"600":[2221,0]},
         "fire":   {"0":[800,4.8],"50":[1140,4.24],"100":[1252,3.85],"200":[1637,2.97],"300":[1934,1.97],"400":[2131,1.0],"500":[2231,0],"600":[2231,0]},
         "ice":    {"0":[850,4.4],"50":[1170,4.00],"100":[1270,3.80],"200":[1650,2.96],"300":[1946,1.96],"400":[2142,1.0],"500":[2242,0],"600":[2242,0]},
         "thunder":{"0":[900,4.0],"50":[1200,3.74],"100":[1287,3.75],"200":[1662,2.95],"300":[1957,1.95],"400":[2152,1.0],"500":[2252,0],"600":[2252,0]}},
    "VI":{"earth":  {"0":[ 950,7.0],"50":[1300,6.0],"100":[1600,5.0],"200":[2100,4.0],"300":[2500,3.00],"400":[2800,2.00],"500":[3000,1],"600":[3100,0]},
         "water":   {"0":[1010,6.5],"50":[1335,5.9],"100":[1630,4.9],"200":[2100,3.9],"300":[2510,2.95],"400":[2805,1.99],"500":[3004,1],"600":[3104,0]},
         "wind":    {"0":[1070,6.0],"50":[1370,5.8],"100":[1660,4.8],"200":[2100,3.8],"300":[2520,2.90],"400":[2810,1.98],"500":[3008,1],"600":[3108,0]},
         "fire":    {"0":[1130,5.5],"50":[1405,5.7],"100":[1690,4.7],"200":[2100,3.7],"300":[2530,2.85],"400":[2815,1.97],"500":[3012,1],"600":[3112,0]},
         "ice":     {"0":[1190,5.0],"50":[1440,5.6],"100":[1720,4.6],"200":[2100,3.6],"300":[2540,2.80],"400":[2820,1.96],"500":[3016,1],"600":[3116,0]},
         "thunder": {"0":[1250,4.5],"50":[1475,5.5],"100":[1750,4.5],"200":[2100,3.5],"300":[2550,2.75],"400":[2825,1.95],"500":[3020,1],"600":[3120,0]}},
    "ja":{"earth":  {"0":[ 750,6.0],"50":[1050,5.00],"100":[1700,3.00],"200":[2000,2.0],"300":[2200,1.0],"400":[2300,0.0],"500":[2300,0.0],"600":[2300,0.0]},
         "water":   {"0":[ 800,5.6],"50":[1080,4.75],"100":[1712,2.98],"200":[2010,2.0],"300":[2210,1.0],"400":[2310,0.0],"500":[2310,0.0],"600":[2310,0.0]},
         "wind":    {"0":[ 850,5.2],"50":[1110,4.50],"100":[1725,2.96],"200":[2021,2.0],"300":[2221,1.0],"400":[2321,0.0],"500":[2321,0.0],"600":[2321,0.0]},
         "fire":    {"0":[ 900,4.8],"50":[1140,4.25],"100":[1737,2.94],"200":[2031,2.0],"300":[2231,1.0],"400":[2331,0.0],"500":[2331,0.0],"600":[2331,0.0]},
         "ice":     {"0":[ 950,4.4],"50":[1170,4.00],"100":[1750,2.92],"200":[2042,2.0],"300":[2242,1.0],"400":[2342,0.0],"500":[2342,0.0],"600":[2342,0.0]},
         "thunder": {"0":[1000,4.0],"50":[1200,3.75],"100":[1762,2.90],"200":[2052,2.0],"300":[2252,1.0],"400":[2352,0.0],"500":[2352,0.0],"600":[2352,0.0]}},
 "helix":{"earth":  {"0":[ 75,2.0],"50":[175,1.0],"100":[225,0],"200":[225,0],"300":[225,0],"400":[225,0],"500":[225,0],"600":[225,0]},
         "water":   {"0":[ 75,2.0],"50":[175,1.0],"100":[225,0],"200":[225,0],"300":[225,0],"400":[225,0],"500":[225,0],"600":[225,0]},
         "wind":    {"0":[ 75,2.0],"50":[175,1.0],"100":[225,0],"200":[225,0],"300":[225,0],"400":[225,0],"500":[225,0],"600":[225,0]},
         "fire":    {"0":[ 75,2.0],"50":[175,1.0],"100":[225,0],"200":[225,0],"300":[225,0],"400":[225,0],"500":[225,0],"600":[225,0]},
         "ice":     {"0":[ 75,2.0],"50":[175,1.0],"100":[225,0],"200":[225,0],"300":[225,0],"400":[225,0],"500":[225,0],"600":[225,0]},
         "thunder": {"0":[ 75,2.0],"50":[175,1.0],"100":[225,0],"200":[225,0],"300":[225,0],"400":[225,0],"500":[225,0],"600":[225,0]},}
    }
    v,m = mv[tier][element][window]
    # print(tier, element, dINT, window, v, m)

    return(m, v, int(window))
