import json
import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    def invalid_response(self, error, status):
        response_body = {
            'error': error,
        }
        return request.make_json_response(response_body, status=status)

    def valid_response(self, data, status, pagination_info=None):
        response_body = {
            'message': "successful",
            'data': data,
        }
        if pagination_info:
            response_body['pagination_info'] = pagination_info
        return request.make_json_response(response_body, status=status)

    # @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    # def post_property(self):
    #     try:
    #         args = request.httprequest.data.decode()
    #         vals = json.loads(args)
    #         if not vals.get('name'):
    #             return self.invalid_response("The name is required", status=400)
    #         res = request.env['property'].sudo().create(vals)
    #         return request.make_json_response({
    #             "message": "Property created",
    #             "id": res.id,
    #             "name": res.name,
    #         }, status=201)
    #     except Exception as error:
    #         return self.invalid_response(str(error), status=400)@http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            if not vals.get('name'):
                return self.invalid_response("The name is required", status=400)

            # res = request.env['property'].sudo().create(vals)
            cr=request.env.cr
            query=""""INSERT INTO property(name,postcode,bedrooms) VALUES('property2 from SQL', '12453',4) returning id, name, postcode"""
            cr.execute(query)
            res=cr.fetchone()
            print(res)
            # if res:
            # return request.make_json_response({
            #     "message": "Property created",
            #     "id": res.id,
            #     "name": res.name,
            # }, status=201)
        except Exception as error:
            return self.invalid_response(str(error), status=400)
    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        vals = request.jsonrequest
        res = request.env['property'].sudo().create(vals)
        return [{"message": "Property created", "id": res.id}]

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_rec = request.env['property'].sudo().browse(property_id)
            if not property_rec.exists():
                return self.invalid_response("Property not found", status=404)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_rec.write(vals)
            return request.make_json_response({
                "message": "Property Updated",
                "id": property_rec.id,
                "name": property_rec.name,
            }, status=200)
        except Exception as error:
            return self.invalid_response(str(error), status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property_rec = request.env['property'].sudo().browse(property_id)
            if not property_rec.exists():
                return self.invalid_response("Property not found", status=404)
            data = {
                "id": property_rec.id,
                "name": property_rec.name,
                "ref": property_rec.ref,
                "description": property_rec.description,
                "bedrooms": property_rec.bedrooms,
            }
            return self.valid_response(data, status=200)
        except Exception as error:
            return self.invalid_response(str(error), status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_rec = request.env['property'].sudo().browse(property_id)
            if not property_rec.exists():
                return self.invalid_response("ID Does Not Exist", status=404)
            property_rec.unlink()
            return request.make_json_response({"message": "Property Deleted"}, status=200)
        except Exception as error:
            return self.invalid_response(str(error), status=400)

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            page = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])

            offset = (page * limit) - limit if page else None
            if params.get('state'):
                property_domain += [('state', '=', params['state'][0])]

            property_recs = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit,
                                                                  order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)

            if not property_recs:
                return self.invalid_response("No properties found", status=404)

            data = [{
                "id": rec.id,
                "name": rec.name,
                "ref": rec.ref,
                "description": rec.description,
                "bedrooms": rec.bedrooms,
            } for rec in property_recs]

            return self.valid_response(data, status=200, pagination_info={
                'page': page if page else 1,
                'limit': limit,
                'pages': math.ceil(property_count / limit) if limit else 1,
                'count': property_count,
            })
        except Exception as error:
            return self.invalid_response(str(error), status=400)