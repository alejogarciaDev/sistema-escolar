import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';

class AuthService {
  static const _tokenKey = 'auth_token';
  static const _userIdKey = 'user_id';
  static const _userNameKey = 'user_name';
  static const _userEmailKey = 'user_email';
  static const _roleIdKey = 'role_id';
  static const _roleNameKey = 'role_name';

  static Future<void> saveSession(User user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, user.token);
    await prefs.setInt(_userIdKey, user.id);
    await prefs.setString(_userNameKey, user.name);
    await prefs.setString(_userEmailKey, user.email);
    await prefs.setInt(_roleIdKey, user.roleId);
    await prefs.setString(_roleNameKey, user.roleName);
  }

  static Future<User?> getSession() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(_tokenKey);
    if (token == null) return null;
    return User(
      id: prefs.getInt(_userIdKey) ?? 0,
      name: prefs.getString(_userNameKey) ?? '',
      email: prefs.getString(_userEmailKey) ?? '',
      roleId: prefs.getInt(_roleIdKey) ?? 0,
      roleName: prefs.getString(_roleNameKey) ?? '',
      token: token,
    );
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }
}
