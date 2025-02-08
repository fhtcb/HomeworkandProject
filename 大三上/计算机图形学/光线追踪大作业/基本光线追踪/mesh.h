#ifndef MESH_H
#define MESH_H

#include "rtweekend.h"
#include "hittable.h"
#include "hittable_list.h"

class mesh : public hittable {
public:
    mesh(const point3& a, const point3& b, const point3& c, shared_ptr<material> mat)
      : a(a), b(b), c(c), mat(mat){
        auto n = cross(b-a, c-a);
        w = n / dot(n, n);
        normal = unit_vector(n);
        area = 0.5 * n.length();

        set_bounding_box();
    }

    virtual void set_bounding_box(){
        auto bbox1 = aabb(a, b);
        auto bbox2 = aabb(a, c);
        bbox = aabb(bbox1, bbox2);
    }

    aabb bounding_box() const override { return bbox; }

    bool hit(const ray& r, interval ray_t, hit_record& rec) const override {
        auto denom = dot(normal, r.direction());

        // No hit if the ray is parallel to the plane.
        if (fabs(denom) < 1e-8)
            return false;

        auto t = dot((a - r.origin()), normal) / denom;
        if (!ray_t.contains(t))
            return false;

        auto intersection = r.at(t);

        vec3 planar_hitpt_vector = intersection - a;
        auto alpha = dot(w, cross(planar_hitpt_vector, c - a));
        auto beta = dot(w, cross(b - a, planar_hitpt_vector));

        if (!is_interior(alpha, beta, rec))
            return false;

        rec.t = t;
        rec.p = intersection;
        rec.mat = mat;
        rec.set_face_normal(r, normal);

        return true;
    }

    virtual bool is_interior(double a, double b, hit_record& rec) const {
        interval unit_interval = interval(0, 1);

        if (!unit_interval.contains(a) || !unit_interval.contains(b) || !unit_interval.contains(a + b))
            return false;

        rec.u = a;
        rec.v = b;
        return true;
    }
    

private:
    point3 a;
    point3 b;
    point3 c;
    vec3 w;
    shared_ptr<material> mat;
    aabb bbox;
    vec3 normal;
    double area;
};


#endif