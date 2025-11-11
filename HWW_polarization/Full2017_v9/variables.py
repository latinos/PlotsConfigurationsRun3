
variables = {}


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
                             'range' : ([0.0, 0.2, 0.4, 0.6, 0.8, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
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
                             'range' : ([0.0, 0.2, 0.4, 0.7, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
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
                             'range' : ([0.0, 0.2, 0.4, 0.6, 1.0],[0.0, 0.05, 0.2, 0.4, 1.0],),
                             'xaxis' : 'Random Forest score: 2D (VBF) Bkg:LL',
                             'fold' : 3
                          }

variables['RF_VBF_2D_Wide']  = {   'name': ('RF_score_VBF_Bkg:RF_score_VBF_LL'),
                                   'range' : ([0.0, 0.2, 1.0],[0.0, 0.125, 0.35, 0.65, 1.0],),
                                   'xaxis' : 'Random Forest score: 2D (VBF) Bkg:LL',
                                   'fold' : 3
                                }

####

variables['dphill_mll']  = {   'name': ('abs(dphill):mll'),
                               'range' : ([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.15],[0.0, 10, 20, 30, 40, 60, 100],),
                               'xaxis' : 'dphill : mll',
                               'fold' : 3
                            }

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


if doSignals:

    variables = {}

    variables['events']  = {   'name': '1',
                               'range' : (1,0,2),
                               'xaxis' : 'events',
                               'fold' : 3
                            }

    variables['RF_0J_2D']  = {   'name': ('RF_score_0J_Bkg:RF_score_0J_TT'),
                                 'range' : ([0.0, 0.2, 0.4, 0.6, 0.8, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                                 'xaxis' : 'Random Forest score: 2D (0J) Bkg:TT',
                                 'fold' : 3
                              }
    
    
    variables['RF_0J_2D_Wide']  = {   'name': ('RF_score_0J_Bkg:RF_score_0J_TT'),
                                      'range' : ([0.0, 0.5, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                                      'xaxis' : 'Random Forest score: 2D (0J) Bkg:TT',
                                      'fold' : 3
                                   }
    
    
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
    
    variables['RF_2J_2D']  = {   'name': ('RF_score_2J_Bkg:RF_score_2J_LL'),
                                 'range' : ([0.0, 0.2, 0.4, 0.7, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                                 'xaxis' : 'Random Forest score: 2D (2J) Bkg:LL',
                                 'fold' : 3
                              }
    
    variables['RF_2J_2D_Wide']  = {   'name': ('RF_score_2J_Bkg:RF_score_2J_LL'),
                                      'range' : ([0.0, 0.5, 1.0],[0.0, 0.05, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],),
                                      'xaxis' : 'Random Forest score: 2D (2J) Bkg:LL',
                                      'fold' : 3
                                   }
    variables['RF_VBF_2D']  = {   'name': ('RF_score_VBF_Bkg:RF_score_VBF_LL'),
                                  'range' : ([0.0, 0.2, 0.4, 0.6, 1.0],[0.0, 0.05, 0.2, 0.4, 1.0],),
                                  'xaxis' : 'Random Forest score: 2D (VBF) Bkg:LL',
                                  'fold' : 3
                               }
    
    variables['RF_VBF_2D_Wide']  = {   'name': ('RF_score_VBF_Bkg:RF_score_VBF_LL'),
                                       'range' : ([0.0, 0.2, 1.0],[0.0, 0.125, 0.35, 0.65, 1.0],),
                                       'xaxis' : 'Random Forest score: 2D (VBF) Bkg:LL',
                                       'fold' : 3
                                    }
    
    #variables['dphill'] = {   'name'  : 'abs(dphill)',
    #                          'range' : (25, 0.0, 3.15),
    #                          'xaxis' : '#Delta#phi_{ll}',
    #                          'fold'  : 3
    #                       }
    #
    #variables['mtw2']  = {   'name': 'mtw2',
    #'range' : (50, 0.,100),
    #                         'xaxis' : 'm_{T}^{W_{2}} [GeV]',
    #                         'fold' : 0
    #                      }
    #
    #variables['dphill_mll']  = {   'name': ('abs(dphill):mll'),
    #                               'range' : ([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.15],[0.0, 10, 20, 30, 40, 60, 100],),
    #                               'xaxis' : 'dphill : mll',
    #                               'fold' : 3
    #                            }
