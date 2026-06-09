import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static String _baseUrl = 'https://api.auraassistant.site';
  static String _campusUrl = 'https://campus.auraassistant.site';

  static Future<void> loadHost() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final saved = prefs.getString('server_ip');
      if (saved != null && saved.trim().isNotEmpty) {
        final val = saved.trim();
        if (val.contains('auraassistant.site')) {
          _baseUrl = 'https://api.auraassistant.site';
          _campusUrl = 'https://campus.auraassistant.site';
        } else if (val.startsWith('http://') || val.startsWith('https://')) {
          _baseUrl = val;
          _campusUrl = val;
        } else {
          _baseUrl = 'http://$val:8001';
          _campusUrl = 'http://$val:8002';
        }
      } else {
        _baseUrl = 'https://api.auraassistant.site';
        _campusUrl = 'https://campus.auraassistant.site';
      }
    } catch (_) {}
  }

  final String? _token;

  ApiService([this._token]);

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  Map<String, String> get _authHeader => {
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  Future<Map<String, dynamic>> login(String email, String password) async {
    final res = await http.post(
      Uri.parse('$_baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    if (res.statusCode != 200) {
      final err = jsonDecode(res.body);
      throw Exception(err['detail'] ?? 'Error de login');
    }
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getUsers() async {
    final res = await http.get(Uri.parse('$_baseUrl/users/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener usuarios');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> getUser(int id) async {
    final res = await http.get(Uri.parse('$_baseUrl/users/$id'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener usuario');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> createUser(Map<String, dynamic> data) async {
    final res = await http.post(Uri.parse('$_baseUrl/users/'), headers: _headers, body: jsonEncode(data));
    if (res.statusCode != 200) throw Exception('Error al crear usuario');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> updateUser(int id, Map<String, dynamic> data) async {
    final res = await http.put(Uri.parse('$_baseUrl/users/$id'), headers: _headers, body: jsonEncode(data));
    if (res.statusCode != 200) throw Exception('Error al actualizar usuario');
    return jsonDecode(res.body);
  }

  Future<void> deleteUser(int id) async {
    final res = await http.delete(Uri.parse('$_baseUrl/users/$id'), headers: _authHeader);
    if (res.statusCode != 200) throw Exception('Error al eliminar usuario');
  }

  Future<List<dynamic>> getRoles() async {
    final res = await http.get(Uri.parse('$_baseUrl/roles/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener roles');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getMaterias() async {
    final res = await http.get(Uri.parse('$_baseUrl/materias/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener materias');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getTareas() async {
    final res = await http.get(Uri.parse('$_campusUrl/tareas/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener tareas');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> createTarea(Map<String, dynamic> data) async {
    final res = await http.post(Uri.parse('$_campusUrl/tareas/'), headers: _headers, body: jsonEncode(data));
    if (res.statusCode != 200) throw Exception('Error al crear tarea');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getMateriales() async {
    final res = await http.get(Uri.parse('$_campusUrl/materiales/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener materiales');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getDocumentos() async {
    final res = await http.get(Uri.parse('$_campusUrl/documentos/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener documentos');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getCompartidos() async {
    final res = await http.get(Uri.parse('$_campusUrl/compartidos/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener compartidos');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getPermisos() async {
    final res = await http.get(Uri.parse('$_baseUrl/permissions/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener permisos');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getUserPermissions(int userId) async {
    final res = await http.get(Uri.parse('$_baseUrl/permissions/user/$userId'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener permisos del usuario');
    return jsonDecode(res.body);
  }

  Future<void> assignPermissionToUser(int permissionId, int userId) async {
    final res = await http.post(
      Uri.parse('$_baseUrl/permissions/assign-user'),
      headers: _headers,
      body: jsonEncode({'permission_id': permissionId, 'user_id': userId}),
    );
    if (res.statusCode != 200) throw Exception('Error al asignar permiso');
  }

  Future<void> removePermissionFromUser(int permissionId, int userId) async {
    final res = await http.delete(
      Uri.parse('$_baseUrl/permissions/assign-user'),
      headers: _headers,
      body: jsonEncode({'permission_id': permissionId, 'user_id': userId}),
    );
    if (res.statusCode != 200) throw Exception('Error al remover permiso');
  }

  Future<Map<String, dynamic>> getAlumnoByDni(String dni) async {
    final res = await http.get(Uri.parse('$_baseUrl/alumnos/$dni'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Alumno no encontrado');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> updateAlumno(String dni, Map<String, dynamic> data) async {
    final res = await http.put(Uri.parse('$_baseUrl/alumnos/$dni'), headers: _headers, body: jsonEncode(data));
    if (res.statusCode != 200) throw Exception('Error al actualizar alumno');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getHistorial(String dni) async {
    final res = await http.get(Uri.parse('$_baseUrl/alumnos/$dni/historial'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener historial');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> addHistorial(String dni, Map<String, dynamic> data) async {
    final res = await http.post(Uri.parse('$_baseUrl/alumnos/$dni/historial'), headers: _headers, body: jsonEncode(data));
    if (res.statusCode != 200) throw Exception('Error al agregar historial');
    return jsonDecode(res.body);
  }

  Future<void> deleteHistorial(int id) async {
    final res = await http.delete(Uri.parse('$_baseUrl/alumnos/historial/$id'), headers: _authHeader);
    if (res.statusCode != 200) throw Exception('Error al eliminar historial');
  }

  Future<List<dynamic>> getCategorias() async {
    final res = await http.get(Uri.parse('$_baseUrl/categories/'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener categorias');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> createCategoria(Map<String, dynamic> data) async {
    final res = await http.post(Uri.parse('$_baseUrl/categories/'), headers: _headers, body: jsonEncode(data));
    if (res.statusCode != 200) throw Exception('Error al crear categoria');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getPedidos() async {
    final res = await http.get(Uri.parse('$_baseUrl/orders/pending'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener pedidos');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> createPedido(Map<String, dynamic> data) async {
    final res = await http.post(Uri.parse('$_baseUrl/orders/'), headers: _headers, body: jsonEncode(data));
    if (res.statusCode != 200) throw Exception('Error al crear pedido');
    return jsonDecode(res.body);
  }

  Future<List<dynamic>> getPrestamos() async {
    final res = await http.get(Uri.parse('$_baseUrl/loans/active'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener prestamos');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> uploadFile(String dni, String filePath) async {
    final uri = Uri.parse('$_baseUrl/archivos/upload');
    final request = http.MultipartRequest('POST', uri);
    if (_token != null) request.headers['Authorization'] = 'Bearer $_token';
    request.fields['dni'] = dni;
    request.files.add(await http.MultipartFile.fromPath('file', filePath));
    final res = await request.send();
    final body = await res.stream.bytesToString();
    if (res.statusCode != 200) throw Exception('Error al subir archivo');
    return jsonDecode(body);
  }

  Future<List<dynamic>> getAlumnosList({int skip = 0, int limit = 50}) async {
    final res = await http.get(Uri.parse('$_baseUrl/alumnos/?skip=$skip&limit=$limit'), headers: _headers);
    if (res.statusCode != 200) throw Exception('Error al obtener alumnos');
    return jsonDecode(res.body);
  }
}
