from datetime import datetime, timedelta

GARDEMOEN, LILLESTROM, OSLO_S, NATIONALTHEATRET, SKOYEN, STABEKK, LYSAKER, SANDVIKA, ASKER, DRAMMEN = range(1,11)

RUTER = {
    "drammen": {
        "stasjoner": [DRAMMEN, ASKER, SANDVIKA, LYSAKER, SKOYEN, NATIONALTHEATRET, OSLO_S, LILLESTROM, GARDEMOEN],
        "segmenter": [13, 6, 6, 3, 4, 18, 12],
    },
    "direkte": {
        "stasjoner": [OSLO_S, GARDEMOEN],
        "segmenter": [19],
    },
    "stabekk": {
        "stasjoner": [STABEKK, SKOYEN, NATIONALTHEATRET, OSLO_S, GARDEMOEN],
        "segmenter": [3, 4, 6, 19],
    },
}

DIREKTE_IDS = {3731, 3732, 3735, 3736}
STABEKK_IDS = {3733, 3734}

def rutetype(avgangs_id):
    if avgangs_id in DIREKTE_IDS:
        return "direkte"
    if avgangs_id in STABEKK_IDS:
        return "stabekk"
    return "drammen"

def lag_stopp(avganger):
    stopp = []
    stopp_id = 1
    for (avgangs_id, tog_nr, togsett, fra, til, avgangstid, plattform) in avganger:
        rute = RUTER[rutetype(avgangs_id)]
        stasjoner = rute["stasjoner"]
        segmenter = rute["segmenter"]

        if fra != stasjoner[0]:
            stasjoner = list(reversed(stasjoner))
            segment = list(reversed(segment))

        tid = datetime.strptime(avgangstid, "%H:%M")
        for i, stasjon in enumerate(stasjoner):
            ankomst = None if i == 0 else tid.strftime("%H:%M")
            avgang_fra_stopp = None if i == len(stasjoner) - 1 else tid.strftime("%H:%M")
            stopp.append((stopp_id, avgangs_id, stasjon, i + 1, ankomst, avgang_fra_stopp)) 
            stopp_id += 1
            if i < len(segmenter):
                tid += timedelta(minutes=segmenter[i])

        return stopp