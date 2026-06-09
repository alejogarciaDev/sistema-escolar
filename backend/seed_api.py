import http.client, json, urllib.parse, sys

def req(method, path, body=None):
    conn = http.client.HTTPConnection('localhost', 8001, timeout=10)
    h = {'Content-Type': 'application/json'} if body else {}
    conn.request(method, path, json.dumps(body) if body else None, h)
    r = conn.getresponse()
    d = r.read().decode()
    try: d = json.loads(d)
    except: pass
    conn.close()
    return r.status, d

# Check existing
s, existing_roles = req('GET', '/roles/')
print('Existing roles:', s, len(existing_roles) if isinstance(existing_roles, list) else existing_roles)

if s == 200 and isinstance(existing_roles, list) and len(existing_roles) == 0:
    print('Creating roles...')
    for name in ['oficina_alumnos', 'panol', 'admin', 'alumno', 'profesor']:
        s, d = req('POST', '/roles/', {'name': name})
        role_id = d.get('id') if isinstance(d, dict) else '?'
        print(f'  {name} -> id={role_id}')

    print('Creating users...')
    req('POST', '/users/', {'name': 'Juan Perez', 'email': 'juan@test.com', 'password': '123', 'role_id': 4})
    req('POST', '/users/', {'name': 'Carlos Profe', 'email': 'profe@test.com', 'password': '123', 'role_id': 5})

    print('Creating subjects...')
    req('POST', '/materias/?nombre=Matematicas&descripcion=Matematicas+Aplicadas', None)
    req('POST', '/materias/?nombre=Lengua&descripcion=Literatura', None)

    print('Creating alumno profile...')
    s, d = req('POST', '/alumnos/', {'dni': '12345678', 'nombre': 'Juan', 'apellido': 'Perez'})
    print(f'  Alumno creado: {d}')

    print('Verify:')
    print('  Roles:', req('GET', '/roles/'))
    print('  Users:', req('GET', '/users/'))
    print('  Materias:', req('GET', '/materias/'))
    print('  Alumnos:', req('GET', '/alumnos/'))
else:
    print('Already seeded or error')

print('Done')
