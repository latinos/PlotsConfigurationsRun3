#ifndef HEADERS_HH
#define HEADERS_HH

using namespace ROOT::VecOps;

template
<typename container>
float Alt(container c, int index, float alt){
    if (index < c.size()) {
        return c[index];
    }
    else{
        return alt;
    }
}

RVec<double> LogVec(RVec<double> vec){
    RVec<double> out; 
    for(auto const & el : vec){
        out.push_back(TMath::Log(el));
    }
    return out;
}

RVec<double> AbsVec(RVec<double> vec){
    RVec<double> out; 
    for(auto const & el : vec){
        out.push_back(TMath::Abs(el));
    }
    return out;
}


RVec<bool> OddVec(RVec<int> vec){
    RVec<bool> out;
    for (auto const & el: vec){
        out.push_back(TMath::Odd(el));
    }
    return out;
}

#endif
