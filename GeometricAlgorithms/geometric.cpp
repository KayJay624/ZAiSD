#include <iostream>
#include <vector>
#include <math.h>
#include <algorithm>

#define dot(u,v)   ((u).x * (v).x + (u).y * (v).y + (u).z * (v).z)
#define norm(v)     sqrt(dot(v,v))            // norm = length of  vector
#define d(u,v)      norm(u-v)                 // distance = norm of difference
#define SMALL_NUM   0.00000001                // anything that avoids division overflow
#define abs(x)     ((x) >= 0 ? (x) : -(x))    //  absolute value

using namespace std;

class Vector
{
  public:
    double x;
    double y;
    double z;

    Vector() : x(0), y(0), z(0) {}
    Vector(double x, double y, double z) : x(x), y(y), z(z) {}

    friend ostream& operator<<(ostream& os, const Vector& v);

    Vector operator*(double scalar)
    {
      return Vector(this->x * scalar, this->y * scalar, this->z * scalar);
    }

    Vector operator+(const Vector& v2)
    {
      return Vector(this->x + v2.x, this->y + v2.y, this->z + v2.z);
    }

    Vector operator-(const Vector& v2)
    {
      return Vector(this->x - v2.x, this->y - v2.y, this->z - v2.z);
    }

    Vector operator*(const Vector& v2)
    {
      return Vector(this->y * v2.z - this->z * v2.y,
                    this->z * v2.x - this->x * v2.z,
                    this->x * v2.y - this->y * v2.x);
    }
};

ostream& operator<<(ostream& os, const Vector& v)
{
    os << "(" << v.x << "," << v.y << "," << v.z << ")";
    return os;
}
/////////////////////////////////////////////////////////////////
class Point
{
  public:
    double x;
    double y;
    double z;

    Point() : x(0), y(0), z(0) {}
    Point(double x, double y, double z) : x(x), y(y), z(z) {}

    friend ostream& operator<<(ostream& os, const Point& p);
    Vector operator-(const Point& p2)
    {
      return Vector(this->x - p2.x, this->y - p2.y, this->z - p2.z);
    }
    Point operator+(const Vector& v)
    {
      return Point(this->x + v.x, this->y + v.y, this->z + v.z);
    }
};

ostream& operator<<(ostream& os, const Point& p)
{
    os << "(" << p.x << "," << p.y << "," << p.z << ")";
    return os;
}
/////////////////////////////////////////////////////////////////
class Face
{
  public:
    Point v1;
    Point v2;
    Point v3;

    Face(Point v1, Point v2, Point v3) : v1(v1), v2(v2), v3(v3) {}

    friend ostream& operator<<(ostream& os, const Face& f);
};

ostream& operator<<(ostream& os, const Face& f)
{
    os << "[" << f.v1 << "," << f.v2 << "," << f.v3 << "]";
    return os;
}
///////////////////////////////////////////////////////////////////////////////////
class Edge
{
  public:
    Point v1;
    Point v2;

    Edge(Point v1, Point v2) : v1(v1), v2(v2) {}

    friend ostream& operator<<(ostream& os, const Edge& e);
};

ostream& operator<<(ostream& os, const Edge& e)
{
    os << "[" << e.v1 << "," << e.v2 << "]";
    return os;
}
///////////////////////////////////////////////////////////////////////////////////
class Solid
{
  public:
    vector<Face> faces;
    int size;

    Solid(const vector<Face>& f) : faces(f), size(f.size()) {}

    friend ostream& operator<<(ostream& os, const Solid& s);
};

ostream& operator<<(ostream& os, const Solid& s)
{
    os << "{";
    for(auto& f : s.faces)
    {
        os << f;
    }
    os << "}";

    return os;
}
//////////////////
class Plane
{
public:
  Point v1;
  Vector n;

  Plane(Face f)
  {
      this->v1 = f.v1;
      Vector u = f.v2 - f.v1;
      Vector v = f.v3 - f.v1;
      this->n = u * v;
  }
};
///////////////////////////////////////////////////////////////////////////////////
double distance(const Point& p1, const Point& p2)
{
    double d = sqrt((p2.x-p1.x)*(p2.x-p1.x) + (p2.y-p1.y)*(p2.y-p1.y) + (p2.z-p1.z)*(p2.z-p1.z));

    return d;
}

double distance(Edge e, Point p)
{
    Vector v = e.v2 - e.v1;
    Vector w = p - e.v2;

    double c1 = dot(w,v);
    if ( c1 <= 0 )
        return d(p, e.v1);

    double c2 = dot(v,v);
    if ( c2 <= c1 )
        return d(p, e.v2);

    double b = c1 / c2;
    Point Pb = e.v1 + (v * b);
    return d(p, Pb);
}

double distance(Edge e1, Edge e2)
{
    Vector   u = e1.v2 - e1.v1;
    Vector   v = e2.v2 - e2.v1;
    Vector   w = e1.v1 - e2.v1;
    float    a = dot(u,u);         // always >= 0
    float    b = dot(u,v);
    float    c = dot(v,v);         // always >= 0
    float    d = dot(u,w);
    float    e = dot(v,w);
    float    D = a*c - b*b;        // always >= 0
    float    sc, sN, sD = D;       // sc = sN / sD, default sD = D >= 0
    float    tc, tN, tD = D;       // tc = tN / tD, default tD = D >= 0

    // compute the line parameters of the two closest points
    if (D < SMALL_NUM) { // the lines are almost parallel
        sN = 0.0;         // force using point P0 on segment S1
        sD = 1.0;         // to prevent possible division by 0.0 later
        tN = e;
        tD = c;
    }
    else {                 // get the closest points on the infinite lines
        sN = (b*e - c*d);
        tN = (a*e - b*d);
        if (sN < 0.0) {        // sc < 0 => the s=0 edge is visible
            sN = 0.0;
            tN = e;
            tD = c;
        }
        else if (sN > sD) {  // sc > 1  => the s=1 edge is visible
            sN = sD;
            tN = e + b;
            tD = c;
        }
    }

    if (tN < 0.0) {            // tc < 0 => the t=0 edge is visible
        tN = 0.0;
        // recompute sc for this edge
        if (-d < 0.0)
            sN = 0.0;
        else if (-d > a)
            sN = sD;
        else {
            sN = -d;
            sD = a;
        }
    }
    else if (tN > tD) {      // tc > 1  => the t=1 edge is visible
        tN = tD;
        // recompute sc for this edge
        if ((-d + b) < 0.0)
            sN = 0;
        else if ((-d + b) > a)
            sN = sD;
        else {
            sN = (-d +  b);
            sD = a;
        }
    }
    // finally do the division to get sc and tc
    sc = (abs(sN) < SMALL_NUM ? 0.0 : sN / sD);
    tc = (abs(tN) < SMALL_NUM ? 0.0 : tN / tD);

    // get the difference of the two closest points
    Vector   dP = w + (u * sc) - (v * tc);  // =  S1(sc) - S2(tc)

    return norm(dP);   // return the closest distance
}

double distance(Face f, Point p)
{
    double sb, sn, sd;
    Point b;
    Plane pl = Plane(f);

    sn = -dot( pl.n, (p - pl.v1));
    sd = dot(pl.n, pl.n);
    sb = sn / sd;

    b = p + (pl.n * sb);
    return d(p, b);
}

double distance(Edge e, Face f)
{
    Edge e1 = Edge(f.v1, f.v2);
    Edge e2 = Edge(f.v2, f.v3);
    Edge e3 = Edge(f.v1, f.v3);

    double d1 = distance(e, e1);
    double d2 = distance(e, e2);
    double d3 = distance(e, e3);

    return min({d1, d2, d3});
}

double distance(Face f1, Face f2)
{
  Edge e1 = Edge(f1.v1, f1.v2);
  Edge e2 = Edge(f1.v2, f1.v3);
  Edge e3 = Edge(f1.v1, f1.v3);

  double d1 = distance(e1, f2);
  double d2 = distance(e2, f2);
  double d3 = distance(e3, f2);

  return  min({d1, d2, d3});
}

double distance(Solid s1, Solid s2)
{
  return 0;
}

///////////////////////////////////////////////////////////////////////////////////
int main()
{
    Point p1 = Point(1,2,3);
    Point p2 = Point(11,12,13);
    Point p3 = Point(10,22,5);
    Point p0 = Point(0, 0, 0);
    Point p4 = Point(1,4,8);
    Point p5 = Point(6,2,34);

    Face f1 = Face(p1, p2, p3);
    Face f2 = Face(p2, p1, p3);
    Face f3 = Face(p3, p2, p1);
    Face f4 = Face(p0, p4, p5);

    Edge e1 = Edge(p1, p2);
    Edge e2 = Edge(p2, p3);
    Edge e3 = Edge(p0, p4);

    vector<Face> faces = {f1,f2,f3};
    Solid s = Solid(faces);

    cout << p1 << endl;
    cout << f1 << endl;
    cout << e1 << endl;
    cout << s << endl;
    cout << distance(p1, p2) << endl;
    cout << distance(e1, p3) << endl;
    cout << distance(e1, e2) << endl;
    cout << distance(f1, p0) << endl;
    cout << "Edge - face: " << distance(e3, f1) << endl;
    cout << "Face - face: " << distance(f1, f4) << endl;
    return 0;

}
