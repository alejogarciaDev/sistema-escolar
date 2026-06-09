import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class AdminDashboard extends StatefulWidget {
  const AdminDashboard({super.key});
  @override
  State<AdminDashboard> createState() => _AdminDashboardState();
}

class _AdminDashboardState extends State<AdminDashboard> with SingleTickerProviderStateMixin {
  late ApiService _api;
  late TabController _tabController;

  List<dynamic> _users = [];
  List<dynamic> _roles = [];
  List<dynamic> _permissions = [];
  List<dynamic> _userPermissions = [];
  int? _selectedUserId;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _init();
  }

  Future<void> _init() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token') ?? '';
    _api = ApiService(token);
    await _loadData();
  }

  Future<void> _loadData() async {
    try {
      _loading = true;
      setState(() {});
      final results = await Future.wait([
        _api.getUsers(),
        _api.getRoles(),
        _api.getPermisos(),
      ]);
      _users = results[0];
      _roles = results[1];
      _permissions = results[2];
      _loading = false;
      setState(() {});
    } catch (e) {
      _loading = false;
      _error = e.toString();
      setState(() {});
    }
  }

  String _roleName(int? roleId) {
    final role = _roles.firstWhere((r) => r['id'] == roleId, orElse: () => {'name': '?'});
    return role['name'] ?? '?';
  }

  Color _roleColor(int? roleId) {
    switch (roleId) {
      case 1: return Colors.red.shade700;
      case 2: return Colors.blue.shade700;
      case 3: return Colors.green.shade700;
      case 4: return Colors.orange.shade700;
      case 5: return Colors.purple.shade700;
      default: return Colors.grey;
    }
  }

  void _showCreateUserDialog() {
    final nameCtrl = TextEditingController();
    final emailCtrl = TextEditingController();
    final passCtrl = TextEditingController();
    int? selectedRole;

    showDialog(context: context, builder: (ctx) => StatefulBuilder(
      builder: (ctx, setD) => AlertDialog(
        title: const Text('Crear Usuario'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Nombre')),
              TextField(controller: emailCtrl, decoration: const InputDecoration(labelText: 'Email')),
              TextField(controller: passCtrl, decoration: const InputDecoration(labelText: 'Contraseña'), obscureText: true),
              const SizedBox(height: 12),
              DropdownButtonFormField<int>(
                decoration: const InputDecoration(labelText: 'Rol'),
                value: selectedRole,
                items: _roles.map((r) => DropdownMenuItem<int>(value: r['id'] as int?, child: Text(r['name'] ?? ''))).toList(),
                onChanged: (v) => setD(() => selectedRole = v),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
          ElevatedButton(
            onPressed: () async {
              if (nameCtrl.text.isEmpty || emailCtrl.text.isEmpty || passCtrl.text.isEmpty || selectedRole == null) return;
              try {
                await _api.createUser({
                  'name': nameCtrl.text,
                  'email': emailCtrl.text,
                  'password': passCtrl.text,
                  'role_id': selectedRole,
                });
                Navigator.pop(ctx);
                await _loadData();
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
              }
            },
            child: const Text('Crear'),
          ),
        ],
      ),
    ));
  }

  void _showEditUserDialog(Map<String, dynamic> user) {
    final nameCtrl = TextEditingController(text: user['name'] ?? '');
    final emailCtrl = TextEditingController(text: user['email'] ?? '');
    final id = user['id'];

    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Editar Usuario'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Nombre')),
          TextField(controller: emailCtrl, decoration: const InputDecoration(labelText: 'Email')),
        ],
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () async {
            try {
              await _api.updateUser(id, {'name': nameCtrl.text, 'email': emailCtrl.text});
              Navigator.pop(ctx);
              await _loadData();
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
            }
          },
          child: const Text('Guardar'),
        ),
      ],
    ));
  }

  void _confirmDelete(int id) {
    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Eliminar Usuario'),
      content: const Text('¿Está seguro de eliminar este usuario?'),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
        ElevatedButton(
          style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
          onPressed: () async {
            try {
              await _api.deleteUser(id);
              Navigator.pop(ctx);
              await _loadData();
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
            }
          },
          child: const Text('Eliminar', style: TextStyle(color: Colors.white)),
        ),
      ],
    ));
  }

  Future<void> _loadUserPermissions(int userId) async {
    try {
      _selectedUserId = userId;
      _userPermissions = await _api.getUserPermissions(userId);
      setState(() {});
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  bool _hasPermission(int permId) {
    return _userPermissions.any((up) => up['permission_id'] == permId || up['id'] == permId);
  }

  void _togglePermission(int permId) async {
    if (_selectedUserId == null) return;
    try {
      if (_hasPermission(permId)) {
        await _api.removePermissionFromUser(permId, _selectedUserId!);
      } else {
        await _api.assignPermissionToUser(permId, _selectedUserId!);
      }
      await _loadUserPermissions(_selectedUserId!);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_error != null) return Center(child: Text('Error: $_error'));

    return Column(
      children: [
        TabBar(
          controller: _tabController,
          labelColor: Colors.orange,
          unselectedLabelColor: Colors.grey,
          indicatorColor: Colors.orange,
          tabs: const [
            Tab(text: 'Usuarios'),
            Tab(text: 'Permisos Dashboard'),
          ],
        ),
        Expanded(
          child: TabBarView(
            controller: _tabController,
            children: [
              _buildUsersTab(),
              _buildPermissionsTab(),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildUsersTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Usuarios', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              ElevatedButton.icon(
                icon: const Icon(Icons.add),
                label: const Text('Nuevo'),
                onPressed: _showCreateUserDialog,
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: ListView.builder(
              itemCount: _users.length,
              itemBuilder: (_, i) {
                final u = _users[i];
                final id = u['id'] ?? 0;
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: _roleColor(u['role_id']),
                      child: Text(
                        (u['name'] as String?)?.substring(0, 1).toUpperCase() ?? '?',
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                    ),
                    title: Text(u['name'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                    subtitle: Text('${u['email'] ?? ''}\nRol: ${_roleName(u['role_id'])}'),
                    isThreeLine: true,
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(icon: const Icon(Icons.edit, color: Colors.blue), onPressed: () => _showEditUserDialog(u)),
                        IconButton(icon: const Icon(Icons.delete, color: Colors.red), onPressed: () => _confirmDelete(id)),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildPermissionsTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Permisos por Usuario', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              if (_selectedUserId != null)
                TextButton(onPressed: () => setState(() { _selectedUserId = null; _userPermissions = []; }), child: const Text('Limpiar')),
            ],
          ),
        ),
        if (_selectedUserId == null)
          Expanded(
            child: ListView.builder(
              itemCount: _users.length,
              itemBuilder: (_, i) {
                final u = _users[i];
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  child: ListTile(
                    title: Text(u['name'] ?? ''),
                    subtitle: Text(_roleName(u['role_id'])),
                    trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: () => _loadUserPermissions(u['id']),
                  ),
                );
              },
            ),
          )
        else
          Expanded(
            child: Column(
              children: [
                Card(
                  color: Colors.orange.shade50,
                  margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Row(
                      children: [
                        const Icon(Icons.person, color: Colors.orange),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            'Editando permisos de:\n${_users.firstWhere((u) => u['id'] == _selectedUserId)['name'] ?? ''}',
                            style: const TextStyle(fontWeight: FontWeight.w600),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: _permissions.length,
                    itemBuilder: (_, i) {
                      final p = _permissions[i];
                      final permId = p['id'] ?? p['permission_id'] ?? 0;
                      final assigned = _hasPermission(permId);
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: ListTile(
                          title: Text(p['name'] ?? 'Permiso #$permId'),
                          subtitle: Text(p['description'] ?? ''),
                          trailing: Switch(
                            value: assigned,
                            activeColor: Colors.orange,
                            onChanged: (_) => _togglePermission(permId),
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
      ],
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}
