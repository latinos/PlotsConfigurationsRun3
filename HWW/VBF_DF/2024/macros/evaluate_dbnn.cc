#ifndef EVALUATE_DBNN
#define EVALUATE_DBNN

#include <vector>
#include <iostream>
#include <stdexcept>
#include <math.h>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "ROOT/RVec.hxx"
#include <Python.h>

using namespace std;
using namespace ROOT;
using namespace ROOT::VecOps;

// 1. Changed return type to RVec<float>
ROOT::RVec<float> evaluate_dbnn(
        float detajj, float dphill, float drll, float mjj, float ht,
        float mth, float mll, float puppimet, float jeteta1, float jeteta2,
        float jetpt1, float jetpt2, float dphillmet, float ptll, float ctot,
        float mlj11, float mlj12, float mlj21, float mlj22, float eta1,
        float eta2, float pt1, float pt2
)
{
    static PyObject* pFunction = nullptr;
    if (!Py_IsInitialized()) {
        Py_Initialize();
    }
    PyGILState_STATE gstate = PyGILState_Ensure();
    if (pFunction == nullptr) {
        PyObject* sysPath = PySys_GetObject("path");
        PyList_Append(sysPath, PyUnicode_DecodeFSDefault("/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationRun3/HWW/VBF_DF/2024/macros"));

        PyObject* pModule = PyImport_ImportModule("load_nn");
        if (pModule == NULL) {
            PyErr_Print();
            PyGILState_Release(gstate);
            throw std::runtime_error("ERROR importing load_nn module");
        }

        pFunction = PyObject_GetAttrString(pModule, "load_dbnn_model");
        Py_DECREF(pModule);
        if (pFunction == NULL) {
            PyErr_Print();
            PyGILState_Release(gstate);
            throw std::runtime_error("ERROR getting load_dbnn_model");
        }
    }

    ROOT::RVec<float> result = {-99.9, -99.9, -99.9, -99.9, -1.0};

    std::vector<float> input = {
        detajj, dphill, drll, mjj, ht, mth, mll, puppimet, jeteta1, jeteta2,
        jetpt1, jetpt2, dphillmet, ptll, ctot, mlj11, mlj12, mlj21, mlj22,
        eta1, eta2, pt1, pt2
    };

    PyObject* pList = PyList_New(input.size());
    for (size_t i = 0; i < input.size(); ++i) {
        PyList_SetItem(pList, i, PyFloat_FromDouble((double)input[i]));
    }
    PyObject* pArgs = PyTuple_Pack(1, pList);
    Py_DECREF(pList);

    if (pArgs != NULL) {
        PyObject* pValue = PyObject_CallObject(pFunction, pArgs);
        if (pValue != NULL) {
            if (PyList_Check(pValue)) {
                Py_ssize_t listSize = PyList_Size(pValue);
                result.clear();
                for (Py_ssize_t i = 0; i < listSize; i++) {
                    PyObject* listItem = PyList_GetItem(pValue, i);
                    result.push_back((float)PyFloat_AsDouble(listItem));
                }
            } else {
                PyErr_Print();
            }
            Py_DECREF(pValue);
        } else {
            PyErr_Print();
        }
        Py_DECREF(pArgs);
    } else {
        PyErr_Print();
    }

    PyGILState_Release(gstate);
    return result; 
}

#endif