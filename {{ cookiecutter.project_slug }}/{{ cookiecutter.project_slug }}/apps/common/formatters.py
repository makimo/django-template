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

            def has_correct_content_type(request):
                CONTENT_TYPES = ['application/json', 'application/x-www-form-urlencoded']
                return record.request.META.get('CONTENT_TYPE', None) in CONTENT_TYPES

            if is_django_request(record.request):
                has_correct_content_type = has_correct_content_type(record.request)

                record.request = {
                    'request': record.request,
                    'headers': record.request.headers
                }

                if has_correct_content_type:
                    record.request['body'] = record.request['request'].body.decode('UTF-8')

        super().add_fields(log_record, record, message_dict)
