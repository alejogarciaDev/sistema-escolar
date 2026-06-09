import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';

class AuthService {
  static const _tokenKey = 'auth_token';
  static const _userIdKey = 'user_id';
  static const _userNameKey = 'user_name';
  static const _userEmailKey = 'user_email';
  static const _roleIdKey = 'role_id';
  static const _roleNameKey = 'role_name';
  static const _dashboardsKey = 'user_dashboards';

  static Future<void> saveSession(User user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, user.token);
    await prefs.setString('token', user.token);
    await prefs.setInt(_userIdKey, user.id);
    await prefs.setString(_userNameKey, user.name);
    await prefs.setString(_userEmailKey, user.email);
    await prefs.setInt(_roleIdKey, user.roleId);
    await prefs.setString(_roleNameKey, user.roleName);
    await prefs.setString(_dashboardsKey, jsonEncode(user.dashboards));
  }

  static Future<User?> getSession() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(_tokenKey);
    if (token == null) return null;
    if (prefs.getString('token') == null) {
      await prefs.setString('token', token);
    }
    List<Map<String, dynamic>> dashboards = [];
    try {
      final raw = prefs.getString(_dashboardsKey);
      if (raw != null) {
        final list = jsonDecode(raw) as List;
        dashboards = list.map((e) => Map<String, dynamic>.from(e)).toList();
      }
    } catch (_) {}
    return User(
      id: prefs.getInt(_userIdKey) ?? 0,
      name: prefs.getString(_userNameKey) ?? '',
      email: prefs.getString(_userEmailKey) ?? '',
      roleId: prefs.getInt(_roleIdKey) ?? 0,
      roleName: prefs.getString(_roleNameKey) ?? '',
      token: token,
      dashboards: dashboards,
    );
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }
}
