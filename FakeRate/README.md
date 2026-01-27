# Fake Rate Estimation

Configurations to estimate fake and prompt rates.

### Run 2 Effective Luminosities

You can find a summary of the Run 2 effective luminosities at this link:
https://github.com/NTrevisani/FakeRateMeasurement/blob/master/certification/BRILCALC.md

### Run 3 Effective Luminosities

Since we are using some pre-scaled triggers, we need to calculate their effective luminosities.

The first thing to do is to get the latest Golden json file(s) for Run 3 collisions. They can be found here:

    https://cms-service-dqmdc.web.cern.ch/CAF/certification/

To get the Full 2022 Golden json file:

    wget https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json -O certification/Cert_Collisions2022_355100_362760_Golden.json

The 2022 data taking period has been split into two eras: `2022` including runs (355100,357900) and `2022EE` including runs (359022,362760). To split the json file accordingly, you can use `jq`:

    jq 'with_entries(select((.key | tonumber) >= 355100 and (.key | tonumber) <= 357900))' certification/Cert_Collisions2022_355100_362760_Golden.json > certification/Cert_Collisions2022_355100_357900_Golden.json

    jq 'with_entries(select((.key | tonumber) >= 359022 and (.key | tonumber) <= 362760))' certification/Cert_Collisions2022_355100_362760_Golden.json > certification/Cert_Collisions2022_359022_362760_Golden.json

Now that we have the required input, we can do the actual effective luminosity measurements. For this, we use brilcalc. You can find all information at this TWiki:

    https://twiki.cern.ch/twiki/bin/view/CMS/BrilcalcQuickStart

Step by step, we start by loading the required environment:

    source /cvmfs/cms-bril.cern.ch/cms-lumi-pog/brilws-docker/brilws-env

Then, we can run it to get the luminosities.

### 2022

    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_355100_357900_Golden.json --hltpath "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v*"
    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_355100_357900_Golden.json --hltpath "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v*"

    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_355100_357900_Golden.json --hltpath "HLT_Mu8_TrkIsoVVL_v*"
    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_355100_357900_Golden.json --hltpath "HLT_Mu17_TrkIsoVVL_v*"

| Trigger path                             | Luminosity [1/pb] |
| :---                                     |              ---: |
| HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 |             5.977 |
| HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 |             5.977 |
| HLT_Mu8_TrkIsoVVL                        |             1.349 |
| HLT_Mu17_TrkIsoVVL                       |             6.207 |

### 2022EE

    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_359022_362760_Golden.json --hltpath "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v*"
    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_359022_362760_Golden.json --hltpath "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v*"

    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_359022_362760_Golden.json --hltpath "HLT_Mu8_TrkIsoVVL_v*"
    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2022_359022_362760_Golden.json --hltpath "HLT_Mu17_TrkIsoVVL_v*"

| Trigger path                             | Luminosity [1/pb] |
| :---                                     |              ---: |
| HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 |            20.228 |
| HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 |            20.228 |
| HLT_Mu8_TrkIsoVVL                        |             4.987 |
| HLT_Mu17_TrkIsoVVL                       |            20.517 |

### 2024

Get the 2024 golden json:

    wget https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions24/Cert_Collisions2024_378981_386951_Golden.json -O certification/Cert_Collisions2024_378981_386951_Golden.json

Get the individual luminosity:

    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2024_378981_386951_Golden.json --hltpath "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v*"
    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2024_378981_386951_Golden.json --hltpath "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v*"

    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2024_378981_386951_Golden.json --hltpath "HLT_Mu8_TrkIsoVVL_v*"
    brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2024_378981_386951_Golden.json --hltpath "HLT_Mu17_TrkIsoVVL_v*"

	brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2024_378981_386951_Golden.json --hltpath "HLT_IsoMu24_v*"
	brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb -i certification/Cert_Collisions2024_378981_386951_Golden.json --hltpath "HLT_Ele30_WPTight_Gsf_v*"

| Trigger path                             | Luminosity [1/pb] |
| :---                                     |              ---: |
| HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 |            70.526 |
| HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 |            70.526 |
| HLT_Mu8_TrkIsoVVL                        |            12.424 |
| HLT_Mu17_TrkIsoVVL                       |            336.40 |
| HLT_IsoMu24                              |            109329 |
| HLT_Ele30_WPTight_Gsf                    |            109315 |