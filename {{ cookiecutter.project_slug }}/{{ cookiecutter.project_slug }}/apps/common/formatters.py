from pythonjsonlogger import jsonlogger


class DjangoRequestJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        if getattr(record, 'request', None):
            if getattr(record.request, 'method', None):
                record.request = {
                    'request': record.request,
                    'headers': record.request.headers,
                    'body': record.request.body.decode('UTF-8')
                }

        super().add_fields(log_record, record, message_dict)
