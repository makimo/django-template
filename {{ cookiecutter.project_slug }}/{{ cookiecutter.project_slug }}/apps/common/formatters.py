from pythonjsonlogger import jsonlogger


class DjangoRequestJsonFormatter(jsonlogger.JsonFormatter):
    """
    This class is used to serialize headers and body of the JSON Django request
    into the `request` property in the record of `jsonlogger.JsonFormatter`.
    """

    def add_fields(self, log_record, record, message_dict):
        if getattr(record, 'request', None):
            def is_django_request(request):
                return getattr(record.request, 'method', None)

            def is_json_request(request):
                return record.request.META.get('CONTENT_TYPE', None) == 'application/json'

            if is_django_request(record.request) and is_json_request(record.request):
                record.request = {
                    'request': record.request,
                    'headers': record.request.headers,
                    'body': record.request.body.decode('UTF-8')
                }

        super().add_fields(log_record, record, message_dict)
