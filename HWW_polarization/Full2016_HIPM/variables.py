
variables = {}


variables['RF_0J_LL']  = {   'name': 'RF_score_0J_LL',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 0J LL',
                             'fold' : 3 
                         } 
variables['RF_0J_TT']  = {   'name': 'RF_score_0J_TT',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 0J TT',
                             'fold' : 3
                         }
variables['RF_0J_Bkg']  = {   'name': 'RF_score_0J_Bkg',
                              'range' : (40,0,1),
                              'xaxis' : 'Random Forest score 0J Background',
                              'fold' : 3
                          }



variables['RF_1J_LL']  = {   'name': 'RF_score_1J_LL',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 1J LL',
                             'fold' : 3
                         }
variables['RF_1J_TT']  = {   'name': 'RF_score_1J_TT',
                             'range' : (40,0,1),
                             'xaxis' : 'Random Forest score 1J TT',
                             'fold' : 3
                         }
variables['RF_1J_Bkg']  = {   'name': 'RF_score_1J_Bkg',
                              'range' : (40,0,1),
                              'xaxis' : 'Random Forest score 1J Background',
                              'fold' : 3
                          }



variables['RF_2J_LL']  = {   'name': 'RF_score_2J_LL',
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



variables['RF_VBF_LL']  = {   'name': 'RF_score_VBF_LL',
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


variables['events']  = {   'name': '1',
                        'range' : (1,0,2),
                        'xaxis' : 'events',
                        'fold' : 3
                        }

'''
variables['BDT_0J']  = {   'name': 'BDTG4D3_0J',
                           'range' : (40,-1,1),
                           'xaxis' : 'BDT 0J',
                           'fold' : 3
                        }
variables['BDT_0J_WP50']  = {   'name': 'BDTG4D3_0J',
                                'range' : (20, 0.5, 1),
                                'xaxis' : 'BDT 0J',
                                'fold' : 0
                        }

variables['BDT_1J']  = {   'name': 'BDTG4D3_1J',
                           'range' : (40,-1,1),
                           'xaxis' : 'BDT 1J',
                           'fold' : 3
                        }
variables['BDT_1J_WP50']  = {   'name': 'BDTG4D3_1J',
                                'range' : (20, 0.5, 1),
                                'xaxis' : 'BDT 1J',
                                'fold' : 0
                        }

variables['BDT_2J']  = {   'name': 'BDTG4D3_2J',
                           'range' : (40,-1,1),
                           'xaxis' : 'BDT 2J',
                           'fold' : 3
                        }
variables['BDT_2J_WP50']  = {   'name': 'BDTG4D3_2J',
                                'range' : (20, 0.5, 1),
                                'xaxis' : 'BDT 2J',
                                'fold' : 0
                        }


variables['BDT_VBF']  = {   'name': 'BDTG4D3_VBF',
                            'range' : (40,-1,1),
                            'xaxis' : 'BDT VBF',
                            'fold' : 3
                        }
variables['BDT_VBF_WP50']  = {   'name': 'BDTG4D3_VBF',
                                'range' : (20, 0.5, 1),
                                'xaxis' : 'BDT VBF',
                                'fold' : 0
                        }


###### POLARIZATION

variables['RF_score_0J_Pol']  = {   'name': 'RF_score_0J_Pol',
                                    'range' : (40, 0.0, 1.0),
                                    'xaxis' : 'Random forest for Polarization 0J (XGBoost)',
                                    'fold' : 3
                                 }

variables['RF_score_1J_Pol']  = {   'name': 'RF_score_1J_Pol',
                                    'range' : (40, 0.0, 1.0),
                                    'xaxis' : 'Random forest for Polarization 1J (XGBoost)',
                                    'fold' : 3
                                 }

variables['RF_score_2J_Pol']  = {   'name': 'RF_score_2J_Pol',
                                    'range' : (40, 0.0, 1.0),
                                    'xaxis' : 'Random forest for Polarization 2J (XGBoost)',
                                    'fold' : 3
                                 }

variables['RF_score_VBF_Pol']  = {   'name': 'RF_score_VBF_Pol',
                                     'range' : (40, 0.0, 1.0),
                                     'xaxis' : 'Random forest for Polarization VBF (XGBoost)',
                                     'fold' : 3
                                  }


#####
variables['events']  = {   'name': '1',      
                        'range' : (1,0,2),  
                        'xaxis' : 'events', 
                        'fold' : 3
                        }


variables['nvtx']  = {   'name': 'PV_npvsGood',
                       'range' : (20,0,100),
                       'xaxis' : 'nvtx',
                        'fold' : 3
                     }
variables['mll']  = {   'name': 'mll',
                        'range' : (40, 20., 100.),
                        'xaxis' : 'm_{ll} [GeV]',
                        'fold' : 3
                        }
variables['mjj'] = {      'name'  : 'mjj',                                                                                                                                                  
                          'range' : (30, 0., 400.),
                          'xaxis' : 'm_{jj} [GeV]',
                          'fold'  : 3
                   }
variables['mth']  = {   'name': 'mth',
                        'range' : (30, 50.,150),
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
variables['mth_DY']  = {   'name': 'mth',
                        'range' : (30, 0, 60),
                        'xaxis' : 'm_{T}^{H} [GeV]',
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
variables['dphill'] = {   'name'  : 'dphill',
                          'range' : (20, 0.0, 2.3),
                          'xaxis' : '#Delta#phi_{ll}',
                          'fold'  : 3
                      }
variables['dphill_2'] = {   'name'  : 'dphill',
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
                          'range' : (30, 0.5, 2.5),
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
'''

