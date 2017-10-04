#include <iostream>
#include <fstream>
#include <vector>

#ifndef CSV_READER
#define CSV_READER

struct Point
{
    double x;
    double y;
};

namespace kjl
{
  std::vector<Point> getPoints(const std::string& fileName)
  {
    std::vector<Point> points;
    std::ifstream ip(fileName);

    if(!ip.is_open())
    {
      std::cout << "ERROR: File Open" << std::endl;
      return points;
    }

    std::string xStr;
    std::string yStr;

    while(ip.good())
    {
      getline(ip, xStr, ',');
      //std::cout << "'" << xStr << "'" << std::endl;

      getline(ip, yStr, '\n');
      //std::cout << "'" << yStr << "'" << std::endl;

      if(xStr == "" || yStr == "")
      {
        break;
      }

      Point p = {std::stod(xStr), std::stod(yStr)};
      points.push_back(p);
    }

    ip.close();

    return points;
  }
}
#endif
