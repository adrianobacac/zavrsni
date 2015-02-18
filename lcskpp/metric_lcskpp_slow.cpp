#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
#include <cstring>

#include "lcskpp.h"
using namespace std;

// Default value of the k parameter.
const int kK = 5;

int main(int argc, char* argv[]) {
	if(argc!=3){
		return -1;
	}
	int lcskpp_sparse_slow_len = 0;
	vector<pair<int, int> > lcskpp_sparse_slow_recon;
	lcskpp_sparse_slow(argv[1], argv[2], kK, &lcskpp_sparse_slow_len,
	                     &lcskpp_sparse_slow_recon);

	std::cout << lcskpp_sparse_slow_len*1.0 / std::max(strlen(argv[1]),strlen(argv[2])) << '\n';
	return 0;
}