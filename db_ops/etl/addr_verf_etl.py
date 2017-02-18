from pyusps import address_information

addr = dict([
    ('address', '23422 Alta Mar TER 48'),
    ('city', 'San Jose'),
    ('state', 'CA'),
])
res = address_information.verify('301PERSO4278', addr)
print (res)
