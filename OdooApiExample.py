# -*- coding: utf-8 -*-
import datetime
import json
import logging

from odoo import http, exceptions
from odoo.http import request

_logger = logging.getLogger(__name__)


def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }


class MengoSchoolRestApi(http.Controller):
    @http.route(
        '/api/auth/',
        type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self, *args, **post):
        try:
            username = post["username"]
        except KeyError:
            raise exceptions.AccessDenied(message='`username` is required.')

        try:
            password = post["password"]
        except KeyError:
            raise exceptions.AccessDenied(message='`password` is required.')

        http.request.session.authenticate(http.request.env.cr.dbname, username, password)
        res = request.env['ir.http'].session_info()
        results = {"session_id": res['session_id']}
        return results

    @http.route('/api/<string:model>/', type='http', auth='user', methods=['GET'], csrf=False)
    def get_student_info(self, model, **params):
        registration_number = params['registration_number']
        try:
            students_rec = request.env[model].search(
                [('registration_number', '=', registration_number), ("state", "=", "open")],
                limit=1, order='create_date desc')
        except KeyError as e:
            msg = "The model `%s` does not exist." % model
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )
        if students_rec:
            students = []
            for rec in students_rec:
                vals = {
                    'id': rec.id,
                    'name': rec.name,
                    'registration_number': rec.registration_number,
                    'course': rec.course_id.name,
                    'year_of_study': rec.year_of_study,
                    'semester': rec.semester
                }
                students.append(vals)
            data = {"status": 200, "response": students, "message": "Success"}
            return http.Response(
                json.dumps(data),
                status=200,
                mimetype='application/json'
            )
        else:
            msg = "Please check if your invoice (`%s`) has been generated. " \
                  "Your registration number does not exist in the accounting books" % registration_number
            data = {"status": 200, "response": msg}
            return http.Response(
                json.dumps(data),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/payment_info/',
        type='json', auth='user', methods=["POST"], csrf=False)
    def post_student_payment_info(self, *args, **post):
        try:
            registration_number = post["registration_number"]
        except KeyError:
            raise exceptions.AccessDenied(message='`Registration` is required.')

        try:
            amount = post["amount"]
        except KeyError:
            raise exceptions.AccessDenied(message='`Amount` is required.')

        try:
            transaction_id = post["transaction_id"]
        except KeyError:
            raise exceptions.AccessDenied(message='`Transaction ID` is required.')

        try:
            channel = post["channel"]
        except KeyError:
            raise exceptions.AccessDenied(message='`Channel` is required.')

        try:
            school_pay_receipt_number = post["school_pay_receipt_number"]
        except KeyError:
            raise exceptions.AccessDenied(message='`School Pay Receipt Number` is required.')

        try:
            year_of_study = post["year_of_study"]
        except KeyError:
            raise exceptions.AccessDenied(message='`Year` is required.')

        try:
            semester = post["semester"]
        except KeyError:
            raise exceptions.AccessDenied(message='`Semester` is required.')

        student_record = request.env['account.invoice'].search(
            [('registration_number', '=', registration_number), ('year_of_study', '=', year_of_study),
             ('semester', '=', semester), ("state", "=", "open")], limit=1)
        if student_record:
            for rec in student_record:
                journal = request.env['account.journal'].search([("name", "=", "School Pay")])
                rec.update({
                    "transaction_id": transaction_id,
                    "channel": channel,
                    "school_pay_receipt_number": school_pay_receipt_number,
                    "date_of_payment": datetime.datetime.now(),
                    "journal_id": journal
                })
                rec.pay_and_reconcile(journal, amount)
            results = {"status": 200, "response": "Success"}
        else:
            msg = "This invoice has already been cleared in the Accounts"
            results = {"status": 200, "response": msg}
        return results
