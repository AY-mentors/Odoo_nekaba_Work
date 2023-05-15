# -*- coding: utf-8 -*-
# from odoo import http


# class ClubManagament(http.Controller):
#     @http.route('/club_managament/club_managament', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/club_managament/club_managament/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('club_managament.listing', {
#             'root': '/club_managament/club_managament',
#             'objects': http.request.env['club_managament.club_managament'].search([]),
#         })

#     @http.route('/club_managament/club_managament/objects/<model("club_managament.club_managament"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('club_managament.object', {
#             'object': obj
#         })
