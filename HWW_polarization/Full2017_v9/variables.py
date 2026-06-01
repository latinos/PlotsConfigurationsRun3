
variables = {}

doFitVariables = True

variables['RF_0J_LL']  = {   'name': 'RF_score_0J_LL',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 0J LL',
                             'fold' : 3 
                         }
variables['RF_0J_TT_fine']  = {   'name': 'RF_score_0J_TT',
                                  'range' : (40,0,1),
                                  'xaxis' : 'Random Forest score 0J TT',
                                  'fold' : 3
                               }
variables['RF_0J_TT']  = {   'name': 'RF_score_0J_TT',
                             #'range' : (40,0,1),
                             'range' : ([0.0,0.15,0.225,0.30,0.35,0.4,0.45,0.5,0.55,0.60,0.65,0.725,1.0],),
                             'xaxis' : 'Random Forest score 0J TT',
                             'fold' : 3
                         }
variables['RF_0J_Bkg']  = {   'name': 'RF_score_0J_Bkg',
                              'range' : (40,0,1),
                              'xaxis' : 'Random Forest score 0J Background',
                              'fold' : 3
                          }

#####

variables['RF_0J_2D']  = {   'name': ('RF_score_0J_Bkg:RF_score_0J_TT'),
                             'range' : ([0.0, 0.2, 0.4, 0.6, 0.8, 1.0],[0.0, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                             'xaxis' : 'Random Forest score: 2D (0J) Bkg:TT',
                             'fold' : 3
                          }


variables['RF_0J_2D_Wide']  = {   'name': ('RF_score_0J_Bkg:RF_score_0J_TT'),
                                  'range' : ([0.0, 0.5, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                                  'xaxis' : 'Random Forest score: 2D (0J) Bkg:TT',
                                  'fold' : 3
                               }

####

variables['RF_1J_LL']  = {   'name': 'RF_score_1J_LL',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 1J LL',
                             'fold' : 3
                         }
variables['RF_1J_TT_fine']  = {   'name': 'RF_score_1J_TT',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 1J TT',
                             'fold' : 3
                         }
variables['RF_1J_TT']  = {   'name': 'RF_score_1J_TT',
                             'range' : ([0.0,0.075,0.15,0.225,0.30,0.35,0.425,0.5,0.575,0.65,0.725,0.825,1.0],),
                             'xaxis' : 'Random Forest score 1J TT',
                             'fold' : 3
                         }
variables['RF_1J_Bkg']  = {   'name': 'RF_score_1J_Bkg',
                              'range' : (40,0,1),
                              'xaxis' : 'Random Forest score 1J Background',
                              'fold' : 3
                          }

##### 

variables['RF_1J_2D']  = {   'name': ('RF_score_1J_Bkg:RF_score_1J_TT'),
                             'range' : ([0.0, 0.2, 0.4, 0.6, 0.8, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                             'xaxis' : 'Random Forest score: 2D (1J) Bkg:TT',
                             'fold' : 3
                          }

variables['RF_1J_2D_Wide']  = {   'name': ('RF_score_1J_Bkg:RF_score_1J_TT'),
                                  'range' : ([0.0, 0.5, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                                  'xaxis' : 'Random Forest score: 2D (1J) Bkg:TT',
                                  'fold' : 3
                               }

####

variables['RF_2J_LL']  = {   'name': 'RF_score_2J_LL',
                             'range' : ([0.0, 0.025, 0.1, 0.225, 0.375, 0.575, 0.8, 1.0],),
                             'xaxis' : 'Random Forest score 2J LL',
                             'fold' : 3
                         }
variables['RF_2J_LL_fine']  = {   'name': 'RF_score_2J_LL',
                                  'range' : (40,0,1),
                                  'xaxis' : 'Random Forest score 2J LL',
                                  'fold' : 3
                         }
variables['RF_2J_TT']  = {   'name': 'RF_score_2J_TT',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 2J TT',
                             'fold' : 3
                         }
variables['RF_2J_Bkg']  = {   'name': 'RF_score_2J_Bkg',
                              'range' : (40,0,1),
                              'xaxis' : 'Random Forest score 2J Background',
                              'fold' : 3
                          }

##### 

variables['RF_2J_2D']  = {   'name': ('RF_score_2J_Bkg:RF_score_2J_LL'),
                             'range' : ([0.0, 0.2, 0.4, 0.7, 1.0],[0.0, 0.2, 0.3, 0.4, 0.6, 1.0],),
                             'xaxis' : 'Random Forest score: 2D (2J) Bkg:LL',
                             'fold' : 3
                          }

variables['RF_2J_2D_Wide']  = {   'name': ('RF_score_2J_Bkg:RF_score_2J_LL'),
                                  'range' : ([0.0, 0.5, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                                  'xaxis' : 'Random Forest score: 2D (2J) Bkg:LL',
                                  'fold' : 3
                               }

####

variables['RF_VBF_LL']  = {   'name': 'RF_score_VBF_LL',
                              'range' : ([0.0, 0.125, 0.35, 0.65, 1.0],),
                              'xaxis' : 'Random Forest score VBF LL',
                              'fold' : 3
                          }
variables['RF_VBF_LL_fine']  = {   'name': 'RF_score_VBF_LL',
                              'range' : (40,0,1),
                              'xaxis' : 'Random Forest score VBF LL',
                              'fold' : 3
                          }
variables['RF_VBF_TT']  = {   'name': 'RF_score_VBF_TT',
                              'range' : (40,0,1),
                              'xaxis' : 'Random Forest score VBF TT',
                              'fold' : 3
                          }
variables['RF_VBF_Bkg']  = {   'name': 'RF_score_VBF_Bkg',
                               'range' : (40,0,1),
                               'xaxis' : 'Random Forest score VBF Background',
                               'fold' : 3
                           }

##### 

variables['RF_VBF_2D']  = {   'name': ('RF_score_VBF_Bkg:RF_score_VBF_LL'),
                              'range' : ([0.0, 0.2, 0.4, 0.6, 1.0],[0.0, 0.3, 0.5, 1.0],),
                              'xaxis' : 'Random Forest score: 2D (VBF) Bkg:LL',
                              'fold' : 3
                          }

variables['RF_VBF_2D_Wide']  = {   'name': ('RF_score_VBF_Bkg:RF_score_VBF_LL'),
                                   'range' : ([0.0, 0.2, 1.0],[0.0, 0.125, 0.35, 0.65, 1.0],),
                                   'xaxis' : 'Random Forest score: 2D (VBF) Bkg:LL',
                                   'fold' : 3
                                }

####

variables['events']  = {   'name': '1',
                        'range' : (1,0,2),
                        'xaxis' : 'events',
                        'fold' : 3
                        }

variables['Ctot']  = {   'name': 'Ctot',
                         'range' : (40,0,5),
                         'xaxis' : 'Collinearity',
                         'fold' : 3
                      }
variables['dphilmet1']  = {   'name': 'abs(dphilmet1)',
			      'range' : (40,0,3.15),
                              'xaxis' : 'dphilmet1',
                              'fold' : 3
                           }
variables['dphilmet2']  = {   'name': 'abs(dphilmet2)',
                              'range' : (40,0,3.15),
			      'xaxis' : 'dphilmet2',
                              'fold' : 3
                           }
variables['dphijj']  = {   'name': 'abs(dphijj)',
                           'range' : (40,0,3.15),
			   'xaxis' : 'dphijj',
                           'fold' : 3
                    }
variables['dphil1j1']  = {   'name': 'abs(dphilep1jet1)',
                             'range' : (40,0,3.15),
			     'xaxis' : 'dphilep1jet1',
                             'fold' : 3
                          }
variables['dphil1j2']  = {   'name': 'abs(dphilep1jet2)',
                             'range' : (40,0,3.15),
                             'xaxis' : 'dphilep1jet2',
                             'fold' : 3
                          }
variables['mTi']  = {   'name': 'mTi',
                        'range' : (40, 0., 150.),
                        'xaxis' : 'm_{T}^{i} [GeV]',
                        'fold' : 3
                     }

#####

#variables['nvtx']  = {   'name': 'PV_npvsGood',
#                       'range' : (20,0,100),
#                       'xaxis' : 'nvtx',
#                        'fold' : 3
#                     }
variables['mll']  = {   'name': 'mll',
                        'range' : (40, 20., 150.),
                        'xaxis' : 'm_{ll} [GeV]',
                        'fold' : 3
                        }
variables['mth']  = {   'name': 'mth',
                        'range' : (30, 40.,150),
                        'xaxis' : 'm_{T}^{H} [GeV]',
                        'fold' : 0
                        }
variables['mtw1']  = {   'name': 'mtw1',
                        'range' : (50, 0.,100),
                         'xaxis' : 'm_{T}^{W_{1}} [GeV]',
                         'fold' : 0
                        }
variables['mtw2']  = {   'name': 'mtw2',
                        'range' : (50, 0.,100),
                         'xaxis' : 'm_{T}^{W_{2}} [GeV]',
                         'fold' : 0
                        }
variables['ptll']  = {   'name': 'ptll',
                        'range' : (50, 0,200),
                        'xaxis' : 'p_{T}^{ll} [GeV]',
                        'fold' : 0
                        }
variables['pt1']  = {   'name': 'Lepton_pt[0]',
                        'range' : (40,20,100),
                        'xaxis' : 'p_{T} 1st lep',
                        'fold'  : 0
                        }
variables['pt2']  = {   'name': 'Lepton_pt[1]',
                        'range' : (40,10,100),
                        'xaxis' : 'p_{T} 2nd lep',
                        'fold'  : 0
                        }
variables['eta1']  = {  'name': 'Lepton_eta[0]',
                        'range' : (30, -2.5, 2.5),
                        'xaxis' : '#eta 1st lep',
                        'fold'  : 3
                        }
variables['eta2']  = {  'name': 'Lepton_eta[1]',
                        'range' : (30, -2.5, 2.5),
                        'xaxis' : '#eta 2nd lep',
                        'fold'  : 3
                        }
variables['phi1']  = {  'name': 'Lepton_phi[0]',
                        'range' : (30,-3.2, 3.2),
                        'xaxis' : '#phi 1st lep',
                        'fold'  : 3
                        }
variables['phi2']  = {  'name': 'Lepton_phi[1]',
                        'range' : (30,-3.2, 3.2),
                        'xaxis' : '#phi 2nd lep',
                        'fold'  : 3
                        }

variables['dphijjmet'] = {'name'  : 'abs(dphijjmet)',
                          'range' : (20, 0., 3.2),
                          'xaxis' : '#Delta#phi_{jjmet}',
                          'fold'  : 3
                         }
variables['dphill'] = {   'name'  : 'abs(dphill)',
                          'range' : (25, 0.0, 3.15),
                          'xaxis' : '#Delta#phi_{ll}',
                          'fold'  : 3
                      }
variables['detall'] = { 'name'  : 'abs(detall)',
                        'range' : (40, 0., 5.),
                        'xaxis' : '|#Delta#eta_{ll}|',
                        'fold'  : 3
                      }
variables['drll'] = {     'name'  : 'drll',
                          'range' : (30, 0.5, 5.0),
                          'xaxis' : '#DeltaR_{ll}',
                          'fold'  : 3}
variables['puppimet']  = {
                        'name': 'PuppiMET_pt',
                        'range' : (20,0,200),
                        'xaxis' : 'puppimet [GeV]',
                        'fold'  : 3
                        }
variables['mpmet']  = {
                        'name': 'mpmet',
                        'range' : (30,0,100),
                        'xaxis' : 'mpmet [GeV]',
                        'fold'  : 3
                        }


########## Binning optimization with Bayesian approach
##
## 0J
##
## bins_tt  = [0, 0.3214737583683709, 0.4254094731601681, 0.5292527484734011, 1]
## bins_bkg = [0, 0.13492120988604822, 0.23011665601511558, 0.5470583814486737, 1]
##
## 1J
##
## bins_tt = [0, 0.19672061645578104, 0.31354284071359945, 0.4141258942731793, 0.5107257447264163, 1]
## bins_bkg = [0, 0.1026765410791885, 0.1379380796316898, 0.1809384682373205, 0.31754277605839965, 1]
##
## 2J
##
## bins_tt  = [0, 0.22610548886473997, 0.3425075470823644, 0.510895124084577, 1]
## bins_bkg = [0, 0.1736356729948692, 0.48711927809337074, 0.8544895837056645, 1]
##
## VBF
##
## bins_tt  = [0, 0.521346107076963, 1]
## bins_bkg = [0, 0.015720777588337297, 0.1830323894467776, 0.8853764567291789, 1]

if doFitVariables:

    variables = {}

    variables['events']  = {   'name': '1',
                               'range' : (1,0,2),
                               'xaxis' : 'events',
                               'fold' : 3
                            }

    variables['RF_0J_2D_BO']  = {   'name': ('RF_score2_0J_Bkg:RF_score2_0J_TT'),
                                    'range' : ([0.0, 0.13, 0.23, 0.55, 1.0],[0.0, 0.27, 0.34, 0.44, 0.54, 1.0],),
                                    'xaxis' : 'Random Forest score: 2D (0J) Bkg:TT',
                                    'fold' : 0
                                 }

    variables['RF_1J_2D_BO']  = {   'name': ('RF_score2_1J_Bkg:RF_score2_1J_TT'),
                                    'range' : ([0, 0.11, 0.19, 0.58, 1.0],[0.0, 0.33, 0.43, 0.54, 1.0],),
                                    'xaxis' : 'Random Forest score: 2D (1J) Bkg:TT',
                                    'fold' : 0
                                 }

    variables['RF_2J_2D_BO']  = {   'name': ('RF_score2_2J_Bkg:RF_score2_2J_LL'),
                                    'range' : ([0.0, 0.13, 0.27, 0.80, 1.0],[0.0, 0.26, 0.44, 1.0],),
                                    'xaxis' : 'Random Forest score: 2D (2J) Bkg:LL',
                                    'fold' : 0
                                 }

    variables['RF_VBF_2D_BO']  = {   'name': ('RF_score2_VBF_Bkg:RF_score2_VBF_LL'),
                                     'range' : ([0.0, 0.0157, 0.15, 0.49, 0.82, 1.0],[0.0, 0.50, 1.0],),
                                     'xaxis' : 'Random Forest score: 2D (VBF) Bkg:LL',
                                     'fold' : 0
                                  }
