#ifndef EVALUATE_DNN_POLARIZATION
#define EVALUATE_DNN_POLARIZATION

#include <vector>
#include <iostream>
#include <TMath.h>
#include <math.h>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

#include "ROOT/RVec.hxx"

#include <Python.h>

using namespace ROOT;
using namespace ROOT::VecOps;

std::vector<RVecF> evaluate_dnn(
				float mll,
				float mth,
				float mtw1,
				float mtw2,
				float mjj,
				float mcollWW,
				float ptll,
				float Ctot,
				RVecF Lepton_pt,
				RVecF Lepton_eta,
				RVecF Lepton_phi,
				float dphilmet1,
				float dphilmet2,
				float dphill,
				float detall,
				float dphijj,
				float detajj,
				float dphilep1jet1,
				float dphilep2jet1,
				float dphilep1jet2,
				float dphilep2jet2,
				float btagDeepFlavB,
				float btagDeepFlavB_1,
				float drll,
				float mpmet,
				float PuppiMET_pt,
				float PuppiMET_phi,
				float D_VBF_QCD,
				float D_VBF_VH,
				float D_QCD_VH,
				float D_VBF_DY
				){
  

  
  Py_Initialize();

  RVecD result_0J = {-1.0, -1.0, -1.0, -1.0, -1.0, -1.0};
  RVecD result_1J = {-1.0, -1.0, -1.0, -1.0, -1.0, -1.0};
  RVecD result_2J = {-1.0, -1.0, -1.0, -1.0, -1.0, -1.0};
  RVecD result_VBF = {-1.0, -1.0, -1.0, -1.0, -1.0, -1.0};

  RVecD result_0J_pol  = {-1.0};
  RVecD result_1J_pol  = {-1.0};
  RVecD result_2J_pol  = {-1.0};
  RVecD result_VBF_pol = {-1.0};
  
  // Import the module
  PyObject* sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_DecodeFSDefault("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/"));
  PyObject* pModule_0jet = PyImport_ImportModule("EvaluateRF_0J");
  PyObject* pModule_1jet = PyImport_ImportModule("EvaluateRF_1J");
  PyObject* pModule_2jet = PyImport_ImportModule("EvaluateRF_2J");
  PyObject* pModule_vbf = PyImport_ImportModule("EvaluateRF_VBF");

  PyObject* pModule_0jet_pol = PyImport_ImportModule("EvaluateRF_0J_Pol");
  PyObject* pModule_1jet_pol = PyImport_ImportModule("EvaluateRF_1J_Pol");
  PyObject* pModule_2jet_pol = PyImport_ImportModule("EvaluateRF_2J_Pol");
  PyObject* pModule_vbf_pol = PyImport_ImportModule("EvaluateRF_VBF_Pol");

  if (pModule_0jet != NULL && pModule_1jet != NULL) {
    // Retrieve the function
    PyObject* pFunction_0jet = PyObject_GetAttrString(pModule_0jet, "load_random_forest_model_0jet");
    PyObject* pFunction_1jet = PyObject_GetAttrString(pModule_1jet, "load_random_forest_model_1jet");
    PyObject* pFunction_2jet = PyObject_GetAttrString(pModule_2jet, "load_random_forest_model_2jet");
    PyObject* pFunction_vbf = PyObject_GetAttrString(pModule_vbf, "load_random_forest_model_vbf");    

    PyObject* pFunction_0jet_pol = PyObject_GetAttrString(pModule_0jet_pol, "load_random_forest_model_0jet_pol");
    PyObject* pFunction_1jet_pol = PyObject_GetAttrString(pModule_1jet_pol, "load_random_forest_model_1jet_pol");
    PyObject* pFunction_2jet_pol = PyObject_GetAttrString(pModule_2jet_pol, "load_random_forest_model_2jet_pol");
    PyObject* pFunction_vbf_pol = PyObject_GetAttrString(pModule_vbf_pol, "load_random_forest_model_vbf_pol");
    
    if (pFunction_0jet != NULL && pFunction_1jet != NULL && pFunction_2jet != NULL && pFunction_vbf != NULL) {
      // Prepare arguments
      
      std::vector<float> input_0J;

      input_0J.push_back(mll);
      input_0J.push_back(mth);
      input_0J.push_back(mtw1);
      input_0J.push_back(mtw2);
      input_0J.push_back(ptll);
      input_0J.push_back(drll);
      input_0J.push_back(dphilmet1);
      input_0J.push_back(dphilmet2);
      input_0J.push_back(dphill);
      input_0J.push_back(PuppiMET_pt);
      input_0J.push_back(PuppiMET_phi);
      input_0J.push_back(detall);
      input_0J.push_back(mpmet);


      std::vector<float> input_1J;

      input_1J.push_back(mll);
      input_1J.push_back(mth);
      input_1J.push_back(mtw1);
      input_1J.push_back(mtw2);
      input_1J.push_back(ptll);
      input_1J.push_back(drll);
      input_1J.push_back(dphilmet1);
      input_1J.push_back(dphilmet2);
      input_1J.push_back(dphill);
      input_1J.push_back(PuppiMET_pt);
      input_1J.push_back(PuppiMET_phi);
      input_1J.push_back(detall);
      input_1J.push_back(mpmet);
      input_1J.push_back(dphilep1jet1);
      input_1J.push_back(dphilep2jet1);
      input_1J.push_back(btagDeepFlavB);
      
      std::vector<float> input_2J;

      input_2J.push_back(mll);
      input_2J.push_back(mth);
      input_2J.push_back(mtw1);
      input_2J.push_back(mtw2);
      input_2J.push_back(ptll);
      input_2J.push_back(drll);
      input_2J.push_back(dphilmet1);
      input_2J.push_back(dphilmet2);
      input_2J.push_back(dphill);
      input_2J.push_back(PuppiMET_pt);
      input_2J.push_back(PuppiMET_phi);
      input_2J.push_back(detall);
      input_2J.push_back(mpmet);
      input_2J.push_back(mjj);
      input_2J.push_back(Ctot);
      input_2J.push_back(detajj);
      input_2J.push_back(dphilep1jet1);
      input_2J.push_back(dphilep2jet1);
      input_2J.push_back(dphilep1jet2);
      input_2J.push_back(dphilep2jet2);
      input_2J.push_back(btagDeepFlavB);
      input_2J.push_back(btagDeepFlavB_1);
      input_2J.push_back(D_VBF_QCD);
      input_2J.push_back(D_VBF_VH);
      input_2J.push_back(D_QCD_VH);
      input_2J.push_back(D_VBF_DY);      
      
      // Input for 0 jet
      PyObject* pList = PyList_New(13);
      for (int i = 0; i < 13; ++i) {
	PyList_SetItem(pList, i, PyFloat_FromDouble((double)input_0J[i]));
      }
      PyObject* pArgs_0J = PyTuple_Pack(1, pList);

      // Input for 1 jet
      PyObject* pList_1J = PyList_New(16);
      for (int i = 0; i < 16; ++i) {
        PyList_SetItem(pList_1J, i, PyFloat_FromDouble((double)input_1J[i]));
      }
      PyObject* pArgs_1J = PyTuple_Pack(1, pList_1J);

      // Input for 2 jets
      PyObject* pList_2J = PyList_New(26);
      for (int i = 0; i < 26; ++i) {
        PyList_SetItem(pList_2J, i, PyFloat_FromDouble((double)input_2J[i]));
      }
      PyObject* pArgs_2J = PyTuple_Pack(1, pList_2J);


      if (pArgs_0J != NULL && pArgs_1J != NULL && pArgs_2J != NULL) {
	// Call the function

	PyObject* pValue_0J = PyObject_CallObject(pFunction_0jet, pArgs_0J);
	PyObject* pValue_1J = PyObject_CallObject(pFunction_1jet, pArgs_1J);
	PyObject* pValue_2J = PyObject_CallObject(pFunction_2jet, pArgs_2J);	
	PyObject* pValue_VBF = PyObject_CallObject(pFunction_vbf, pArgs_2J);

	PyObject* pValue_0J_pol  = PyObject_CallObject(pFunction_0jet_pol, pArgs_0J);
        PyObject* pValue_1J_pol  = PyObject_CallObject(pFunction_1jet_pol, pArgs_1J);
        PyObject* pValue_2J_pol  = PyObject_CallObject(pFunction_2jet_pol, pArgs_2J);
        PyObject* pValue_VBF_pol = PyObject_CallObject(pFunction_vbf_pol, pArgs_2J);
	
	if (pValue_0J != NULL && pValue_1J != NULL && pValue_2J != NULL && pValue_VBF != NULL) {

	  // 0 Jet
	  if (PyList_Check(pValue_0J)) {
	    Py_ssize_t listSize = PyList_Size(pValue_0J);

	    for (Py_ssize_t i = 0; i < listSize; i++) {
	      PyObject* listItem = PyList_GetItem(pValue_0J, i);
	      result_0J[i] = PyFloat_AsDouble(listItem);
	    }
	  } else {
	    PyErr_Print();
	  }	  

	  // 1 Jet
          if (PyList_Check(pValue_1J)) {
            Py_ssize_t listSize_1J = PyList_Size(pValue_1J);

            for (Py_ssize_t i = 0; i < listSize_1J; i++) {
              PyObject* listItem_1J = PyList_GetItem(pValue_1J, i);
              result_1J[i] = PyFloat_AsDouble(listItem_1J);
            }
          } else {
            PyErr_Print();
          }


	  // 2 Jet
	  if (PyList_Check(pValue_2J)) {
            Py_ssize_t listSize_2J = PyList_Size(pValue_2J);

            for (Py_ssize_t i = 0; i < listSize_2J; i++) {
              PyObject* listItem_2J = PyList_GetItem(pValue_2J, i);
              result_2J[i] = PyFloat_AsDouble(listItem_2J);
            }
          } else {
            PyErr_Print();
          }
	  
	  // VBF
	  if (PyList_Check(pValue_VBF)) {
            Py_ssize_t listSize_VBF = PyList_Size(pValue_VBF);

            for (Py_ssize_t i = 0; i < listSize_VBF; i++) {
              PyObject* listItem_VBF = PyList_GetItem(pValue_VBF, i);
              result_VBF[i] = PyFloat_AsDouble(listItem_VBF);
            }
          } else {
            PyErr_Print();
          }

	  //// 0J Pol
	  if (PyList_Check(pValue_0J_pol)) {
            Py_ssize_t listSize_pol = PyList_Size(pValue_0J_pol);

            for (Py_ssize_t i = 0; i < listSize_pol; i++) {
              PyObject* listItem_pol = PyList_GetItem(pValue_0J_pol, i);
              result_0J_pol[i] = PyFloat_AsDouble(listItem_pol);
            }
          } else {
            PyErr_Print();
          }

	  //// 1J Pol
	  if (PyList_Check(pValue_1J_pol)) {
            Py_ssize_t listSize_1J_pol = PyList_Size(pValue_1J_pol);

            for (Py_ssize_t i = 0; i < listSize_1J_pol; i++) {
              PyObject* listItem_1J_pol = PyList_GetItem(pValue_1J_pol, i);
              result_1J_pol[i] = PyFloat_AsDouble(listItem_1J_pol);
            }
          } else {
            PyErr_Print();
          }

	  //// 2J Pol
	  if (PyList_Check(pValue_2J_pol)) {
            Py_ssize_t listSize_2J_pol = PyList_Size(pValue_2J_pol);

            for (Py_ssize_t i = 0; i < listSize_2J_pol; i++) {
              PyObject* listItem_2J_pol = PyList_GetItem(pValue_2J_pol, i);
              result_2J_pol[i] = PyFloat_AsDouble(listItem_2J_pol);
            }
          } else {
            PyErr_Print();
          }

	  //// VBF Pol 
	  if (PyList_Check(pValue_VBF_pol)) {
	    Py_ssize_t listSize_VBF_pol = PyList_Size(pValue_VBF_pol);

            for (Py_ssize_t i = 0; i < listSize_VBF_pol; i++) {
              PyObject* listItem_VBF_pol = PyList_GetItem(pValue_VBF_pol, i);
              result_VBF_pol[i] = PyFloat_AsDouble(listItem_VBF_pol);
            }
          } else {
            PyErr_Print();
          }
	  
		  
	} else {
	  PyErr_Print();
	}
	
	Py_DECREF(pArgs_0J);
      } else {
	PyErr_Print();
      }
      
      Py_DECREF(pFunction_0jet);
    } else {
      PyErr_Print();
    }
    
    Py_DECREF(pModule_0jet);
  } else {
    PyErr_Print();
  }

  std::vector<RVecF> results = {ROOT::RVecF(6, -1.0),ROOT::RVecF(6, -1.0),ROOT::RVecF(6, -1.0),ROOT::RVecF(6, -1.0), ROOT::RVecF(6, -1.0),ROOT::RVecF(6, -1.0),ROOT::RVecF(6, -1.0),ROOT::RVecF(6, -1.0)};

  // Debug -------
  //cout << "Test performance" << endl;
  //cout << result_0J << endl;
  //cout << result_1J << endl;
  //cout << result_2J << endl;
  //cout << result_VBF << endl;

  //cout << result_0J_pol << endl;
  //cout << result_1J_pol << endl;
  //cout << result_2J_pol << endl;
  //cout << result_VBF_pol << endl;

  results[0][0] = (float)result_0J[0];
  results[0][1] = (float)result_0J[1];
  results[0][2] = (float)result_0J[2];
  results[0][3] = (float)result_0J[3];
  results[0][4] = (float)result_0J[4];
  results[0][5] = (float)result_0J[5];

  results[1][0] = (float)result_1J[0];
  results[1][1] = (float)result_1J[1];
  results[1][2] = (float)result_1J[2];
  results[1][3] = (float)result_1J[3];
  results[1][4] = (float)result_1J[4];
  results[1][5] = (float)result_1J[5];

  results[2][0] = (float)result_2J[0];
  results[2][1] = (float)result_2J[1];
  results[2][2] = (float)result_2J[2];
  results[2][3] = (float)result_2J[3];
  results[2][4] = (float)result_2J[4];
  results[2][5] = (float)result_2J[5];

  results[3][0] = (float)result_VBF[0];
  results[3][1] = (float)result_VBF[1];
  results[3][2] = (float)result_VBF[2];
  results[3][3] = (float)result_VBF[3];
  results[3][4] = (float)result_VBF[4];
  results[3][5] = (float)result_VBF[5];

  results[4][0] = (float)result_0J_pol[0];

  results[5][0] = (float)result_1J_pol[0];

  results[6][0] = (float)result_2J_pol[0];

  results[7][0] = (float)result_VBF_pol[0];
  
  return results;
  
  Py_Finalize();
  
}

#endif
