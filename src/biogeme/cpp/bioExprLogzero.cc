//-*-c++-*------------------------------------------------------------
//
// File name : bioExprLogzero.cc
// @date   Mon Oct 24 09:48:09 2022
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#include "bioExprLogzero.h"
#include "bioDebug.h"
#include "bioExceptions.h"
#include <cmath>
#include <sstream>

bioExprLogzero::bioExprLogzero(bioExpression* c) :
  child(c) {
  listOfChildren.push_back(c) ;
}

bioExprLogzero::~bioExprLogzero() {
  
}

const bioDerivatives* bioExprLogzero::getValueAndDerivatives(std::vector<bioUInt> literalIds,
							     bioBoolean gradient,
							     bioBoolean hessian) {
  
  
  theDerivatives.with_g = gradient ;
  theDerivatives.with_h = hessian ;
  
  bioUInt n = literalIds.size() ;
  theDerivatives.resize(n) ;
  
  const bioDerivatives* childResult = child->getValueAndDerivatives(literalIds,gradient,hessian) ;
  bioReal cf = childResult->f ;

  if (cf == 0) {
    theDerivatives.f = 0.0 ;
    if (gradient) {
      for (bioUInt i = 0 ; i < n ; ++i) {
	theDerivatives.g[i] = 0.0 ;
	if (hessian) {
	  for (bioUInt j = 0 ; j < n ; ++j) {
	    theDerivatives.h[i][j] = 0.0 ;
	  }
	}
      }
    }
    return &theDerivatives ;
  }
  
  if (cf < 0) {
    if (std::abs(cf) < 1.0e-6) {
      cf = 0.0 ;
    }
    else {
      std::stringstream str ;
      str << "Current values of the literals: " << std::endl ;
      std::map<bioString,bioReal> m = getAllLiteralValues() ;
      for (std::map<bioString,bioReal>::iterator i = m.begin() ;
	   i != m.end() ;
	   ++i) {
	str << i->first << " = " << i->second << std::endl ;
      }
      if (rowIndex != NULL) {
	str << "row number: " << *rowIndex << ", ";
      }
      
      str << "Cannot take the log of a non positive number [" << childResult->f << "]" << std::endl ;
      throw bioExceptions(__FILE__,__LINE__,str.str()) ;
    }
  }
  if (cf == 0.0) {
    theDerivatives.f = -std::numeric_limits<bioReal>::max() / 2.0 ;
  }
  else {    
    theDerivatives.f = log(cf) ;
  }
  if (gradient) {
    for (bioUInt i = 0 ; i < n ; ++i) {
      theDerivatives.g[i] = childResult->g[i] / cf ;
      if (hessian) {
	for (bioUInt j = 0 ; j < n ; ++j) {
	  bioReal fsquare = cf * cf ;
	  if (cf != 0.0) { 
	    theDerivatives.h[i][j] = childResult->h[i][j] / cf -  childResult->g[i] *  childResult->g[j] / fsquare ;
	  }
	  else {
	    theDerivatives.h[i][j] = -std::numeric_limits<bioReal>::max() / 2.0 ;
	  }
	}
      }
    }
  }
  return &theDerivatives ;
}

bioString bioExprLogzero::print(bioBoolean hp) const {
  std::stringstream str ; 
  str << "logzero(" << child->print(hp) << ")";
  return str.str() ;
}

