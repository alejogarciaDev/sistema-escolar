class User {
  final int id;
  final String name;
  final String email;
  final int roleId;
  final String roleName;
  final String token;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.roleId,
    required this.roleName,
    required this.token,
  });

  factory User.fromLogin(Map<String, dynamic> json, String token) {
    final user = json['user'] ?? json;
    return User(
      id: user['id'] ?? 0,
      name: user['name'] ?? json['name'] ?? '',
      email: user['email'] ?? json['email'] ?? '',
      roleId: user['role'] ?? user['role_id'] ?? json['role'] ?? json['role_id'] ?? 0,
      roleName: user['role_name'] ?? json['role_name'] ?? '',
      token: token,
    );
  }

  bool get isAdmin => roleId == 3;
  bool get isAlumno => roleId == 4;
  bool get isProfesor => roleId == 5;
  bool get isPanol => roleId == 2;
  bool get isOficinaAlumnos => roleId == 1;
}
