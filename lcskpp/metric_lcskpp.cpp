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
const int kK = 10;

int main(int argc, char* argv[]) {
	if(argc!=3){
		return -1;
	}
	int lcskpp_length = 0;
	lcskpp_slow(argv[1], argv[2], kK, &lcskpp_length);
	std::cout << lcskpp_length*1.0 / std::max(strlen(argv[1]),strlen(argv[2])) << '\n';
	return 0;
}