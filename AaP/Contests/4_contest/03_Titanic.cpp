#include <iostream>
#include <fstream>
#include<string>
#include<map>
#include<vector>
#include<algorithm>

bool comp(std::map<int, std::string> a, std::map<int, std::string> b) {
  if (std::stoi(a[5]) == std::stoi(b[5])) {
    return a[3] < b[3];
  }
  return std::stoi(a[5]) < std::stoi(b[5]);
}
std::map<int,std :: string> func(std :: string a) {
  int k = 0;
  bool f = true;
  bool f_ = false;
  std::string buf = "";
  std::map<int, std::string> b;
  for (auto i : a) {
    if (i == ',') {
      if (f or f_) {
        b[k] = buf;
        buf = "";
        k += 1;
      }
      else {
        buf += i;
      }
    }
    else if (i == '\"' and f) {
      f = false;
    }
    else if (i == '\"' and f_) {
      buf += "\"";
      f_ = false;
    }
    else if (i == '\"') {
      f_ = true;
    }
    else {
      buf += i;
    }
  }
  return b;
}

int main() {
  std :: ifstream ip("train.csv");
  std :: string line;
  std::vector<std::map<int, std::string>> arr;
  int age;
  int pcclass;
  std::cin >> pcclass;
  std::cin >> age;
  getline(ip, line, '\r');
  while (not ip.eof()) {
    getline(ip, line, '\r');
    std::map<int, std::string> buf_map = func(line);
    if (buf_map[4] == "" or buf_map[2] == "" or buf_map[5] == "") {
      continue;
    }
    if (buf_map[4] == "female" and pcclass == std :: stoi(buf_map[2]) and std :: stoi(buf_map[5]) > age) {
      arr.push_back(buf_map);
    }
  }
  ip.close();
  std::sort(arr.begin(), arr.end(), comp);
  for (auto i : arr) {
    std::cout << i[3] << '\n';
  }
}
