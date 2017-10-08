#include <iostream>
#include <stack>
#include <stdlib.h>
#include <vector>
#include <algorithm>
#include "csvReader.h"

using namespace std;

Point p0;

void findBottomMost(std::vector<Point>& points)
{
  double minYValue = points[0].y;
  int minYIndex = 0;

  for(int i = 1; i < points.size(); i++)
  {
    double y = points[i].y;
    if(y < minYValue ||
      (y == minYValue && points[i].x < points[minYIndex].x))
    {
      minYValue = y;
      minYIndex = i;
    }
  }

  p0 = points[minYIndex];
  std::swap(points[0], points[minYIndex]);
}

double dist(Point p1, Point p2)
{
    return (p1.x - p2.x)*(p1.x - p2.x) +
           (p1.y - p2.y)*(p1.y - p2.y);
}

int orientation(Point p1, Point p2, Point p3)
{
    double d = (p2.y - p1.y) * (p3.x - p2.x) -
               (p2.x - p1.x) * (p3.y - p2.y);


    if(d == 0) // wspolliniowe
    {
      return 0;
    }

    if(d > 0) // na prawo
    {
      return 1;
    }
    else      // na lewo
    {
      return -1;
    }
}

bool compare(Point& p1, Point& p2)
{
   int o = orientation(p0, p1, p2);
   if (o == 0)
   {
     if(dist(p0, p2) >= dist(p0, p1))
     {
       return true;
     }
     else
     {
       return false;
     }
   }

   return (o == -1)? true : false;
}

void sortAngles(std::vector<Point>& points)
{
  std::sort(++points.begin(), points.end(), compare);
}

Point nextToTop(std::stack<Point>& S)
{
    Point p = S.top();
    S.pop();
    Point next = S.top();
    S.push(p);
    return next;
}

void removeSameAnglePoints(std::vector<Point>& points)
{
  std::vector<Point> result;
  for (int i = 1; i < points.size()-1; i++)
  {
     while (i < points.size() &&
            orientation(p0, points[i], points[i+1]) == 0)
     {
         points.erase(points.begin() + i);
     }
  }
}

std::stack<Point> graham(std::vector<Point> points)
{
   int n = points.size();

   std::stack<Point> S;
   S.push(points[0]);
   S.push(points[1]);

   int i = 2;
   while(i < n)
   {
      while (orientation(nextToTop(S), S.top(), points[i]) != -1)
      {
         S.pop();
      }
      S.push(points[i]);
      i++;
   }

  return S;
}

int main()
{
    std::vector<Point> pointsVec = kjl::getPoints("punktyPrzykladowe.csv");

    findBottomMost(pointsVec);
    sortAngles(pointsVec);
    removeSameAnglePoints(pointsVec);
    std::cout << "p0 = (" << p0.x << "," << p0.y << ")" << std::endl << std::endl;

    std::cout << "Points after sorting:" << std::endl;
    for(auto& s : pointsVec)
    {
      std::cout << "(" << s.x << "," << s.y << ")" << std::endl;
    }
    std::cout << std::endl;

    std::stack<Point> S = graham(pointsVec);
    std::cout << "Final result:" << std::endl;
    while (!S.empty())
    {
        Point p = S.top();
        cout << "(" << p.x << ", " << p.y <<")" << endl;
        S.pop();
    }

    return 0;
}
