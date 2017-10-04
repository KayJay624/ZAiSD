#include <iostream>
#include <stack>
#include <stdlib.h>
#include <vector>
#include "csvReader.h"

using namespace std;

Point p0;

void swap(Point &p1, Point &p2)
{
    Point temp = p1;
    p1 = p2;
    p2 = temp;
}

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
}

int dist(Point p1, Point p2)
{
    return (p1.x - p2.x)*(p1.x - p2.x) +
           (p1.y - p2.y)*(p1.y - p2.y);
}

int det(Point p1, Point p2, Point p3)
{
    int val = (p2.y - p1.y) * (p3.x - p2.x) -
              (p2.x - p1.x) * (p3.y - p2.y);

    if (val == 0) return 0;
    return (val > 0)? 1: 2;
}

int compare(const void *vp1, const void *vp2)
{
   Point *p1 = (Point *)vp1;
   Point *p2 = (Point *)vp2;

   int o = det(p0, *p1, *p2);
   if (o == 0)
     return (dist(p0, *p2) >= dist(p0, *p1))? -1 : 1;

   return (o == 2)? -1: 1;
}


void sortAngles(std::vector<Point>& points)
{
  swap(points[0], p0);
  qsort(&points[1], points.size()-1, sizeof(Point), compare);
}

Point nextToTop(std::stack<Point>& S)
{
    Point p = S.top();
    S.pop();
    Point res = S.top();
    S.push(p);
    return res;
}

void graham(std::vector<Point> points)
{
   int m = 1;
   for (int i=1; i<points.size(); i++)
   {
       while (i < points.size()-1 &&
              det(p0, points[i], points[i+1]) == 0)
       {
           i++;
       }

       points[m] = points[i];
       m++;
   }
   
   if (m < 3) return;

   stack<Point> S;
   S.push(points[0]);
   S.push(points[1]);
   S.push(points[2]);

   for (int i = 3; i < m; i++)
   {
      while (det(nextToTop(S), S.top(), points[i]) != 2)
      {
         S.pop();
      }
      S.push(points[i]);
   }

   while (!S.empty())
   {
       Point p = S.top();
       cout << "(" << p.x << ", " << p.y <<")" << endl;
       S.pop();
   }
}

int main()
{
    std::vector<Point> pointsVec = kjl::getPoints("points.csv");

    // for(auto& p : pointsVec)
    // {
    //   std::cout << "(" << p.x << "," << p.y << ")" << std::endl;
    // }

    findBottomMost(pointsVec);
    sortAngles(pointsVec);
    graham(pointsVec);

    return 0;
}
