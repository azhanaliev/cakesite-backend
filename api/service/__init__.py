__author__ = 'Azamatshekin'


def call(service_name, bag):
    if hasattr(service_name, '__call__'):
        return service_name(bag)
    module = service_name.split('.')
    m = __import__('api.service.' + module[0])
    m = getattr(m, 'service')
    m = getattr(m, module[0])
    m = getattr(m, module[1])
    return m(bag)