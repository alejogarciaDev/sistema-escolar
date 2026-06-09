import 'dart:async';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import 'login_screen.dart';
import 'admin_dashboard.dart';
import 'profesor_dashboard.dart';
import 'alumno_dashboard.dart';
import 'panol_dashboard.dart';
import 'oficina_dashboard.dart';

class HomeScreen extends StatefulWidget {
  final User user;
  const HomeScreen({super.key, required this.user});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late List<Map<String, dynamic>> _dashboards;
  int _currentIndex = 0;
  int _unreadCount = 0;
  List<dynamic> _notifications = [];
  bool _notifLoading = false;
  Timer? _notifTimer;
  late ApiService _api;

  static const _dashboardIcons = {
    'admin': Icons.admin_panel_settings,
    'profesor': Icons.school,
    'alumno': Icons.person,
    'panol': Icons.inventory_2,
    'ofalumnos': Icons.folder,
  };

  static const _dashboardColors = {
    'admin': Colors.green,
    'profesor': Colors.purple,
    'alumno': Colors.orange,
    'panol': Colors.blue,
    'ofalumnos': Colors.teal,
  };

  @override
  void initState() {
    super.initState();
    _dashboards = _getAvailableDashboards();
    _api = ApiService(null);
    _loadUnreadCount();
    _notifTimer = Timer.periodic(const Duration(seconds: 30), (_) => _loadUnreadCount());
  }

  List<Map<String, dynamic>> _getAvailableDashboards() {
    if (widget.user.dashboards.isNotEmpty) {
      return widget.user.dashboards;
    }
    return _defaultDashboardsForRole();
  }

  List<Map<String, dynamic>> _defaultDashboardsForRole() {
    final user = widget.user;
    final list = <Map<String, dynamic>>[];
    if (user.isAdmin) list.add({'id': 'admin', 'label': 'Panel Admin'});
    if (user.isPanol) list.add({'id': 'panol', 'label': 'Panel Pañol'});
    if (user.isProfesor) list.add({'id': 'profesor', 'label': 'Panel Profesor'});
    if (user.isAlumno) list.add({'id': 'alumno', 'label': 'Panel Alumno'});
    if (user.isOficinaAlumnos) list.add({'id': 'ofalumnos', 'label': 'Oficina Alumnos'});
    if (list.isEmpty) list.add({'id': 'alumno', 'label': 'Panel Alumno'});
    return list;
  }

  Future<void> _loadUnreadCount() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('token');
      if (token == null) return;
      _api = ApiService(token);
      final count = await _api.getUnreadNotificationCount();
      if (mounted) setState(() => _unreadCount = count);
    } catch (_) {}
  }

  Future<void> _loadNotifications() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('token');
      if (token == null) return;
      _api = ApiService(token);
      _notifLoading = true;
      setState(() {});
      final list = await _api.getNotifications();
      if (mounted) setState(() {
        _notifications = list;
        _notifLoading = false;
      });
    } catch (_) {
      if (mounted) setState(() => _notifLoading = false);
    }
  }

  Future<void> _showNotifications() async {
    await _loadNotifications();
    if (!mounted) return;
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Notificaciones'),
        content: SizedBox(
          width: double.maxFinite,
          child: _notifLoading
              ? const Center(child: CircularProgressIndicator())
              : _notifications.isEmpty
                  ? const Center(child: Text('Sin notificaciones'))
                  : ListView.builder(
                      shrinkWrap: true,
                      itemCount: _notifications.length,
                      itemBuilder: (_, i) {
                        final n = _notifications[i];
                        return ListTile(
                          leading: Icon(
                            n['read'] == true ? Icons.notifications_none : Icons.notifications_active,
                            color: n['read'] == true ? Colors.grey : Colors.orange,
                          ),
                          title: Text(n['title'] ?? '', style: const TextStyle(fontSize: 14)),
                          subtitle: Text(n['message'] ?? '', style: const TextStyle(fontSize: 12)),
                          dense: true,
                          onTap: () {
                            if (n['read'] != true) {
                              _api.markNotificationRead(n['id']);
                              setState(() {
                                n['read'] = true;
                                _unreadCount = (_unreadCount - 1).clamp(0, 999);
                              });
                            }
                          },
                        );
                      },
                    ),
        ),
        actions: [
          if (_notifications.any((n) => n['read'] != true))
            TextButton(
              onPressed: () async {
                await _api.markAllNotificationsRead();
                setState(() {
                  for (var n in _notifications) n['read'] = true;
                  _unreadCount = 0;
                });
                if (ctx.mounted) Navigator.pop(ctx);
              },
              child: const Text('Marcar todas leídas'),
            ),
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cerrar')),
        ],
      ),
    ).then((_) => _loadUnreadCount());
  }

  Widget _buildDashboard(int index) {
    if (index < 0 || index >= _dashboards.length) {
      return const Center(child: Text('Dashboard no disponible'));
    }
    final id = _dashboards[index]['id'] as String;
    switch (id) {
      case 'admin':
        return const AdminDashboard();
      case 'profesor':
        return const ProfesorDashboard();
      case 'alumno':
        return const AlumnoDashboard();
      case 'panol':
        return const PanolDashboard();
      case 'ofalumnos':
        return const OficinaAlumnosDashboard();
      default:
        return const Center(child: Text('Dashboard no implementado'));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_dashboards[_currentIndex]['label'] ?? 'Dashboard'),
        backgroundColor: const Color(0xFF9b0b0b),
        foregroundColor: Colors.white,
        actions: [
          Stack(
            children: [
              IconButton(
                icon: const Icon(Icons.notifications),
                onPressed: _showNotifications,
              ),
              if (_unreadCount > 0)
                Positioned(
                  right: 6,
                  top: 6,
                  child: Container(
                    padding: const EdgeInsets.all(4),
                    decoration: const BoxDecoration(
                      color: Colors.red,
                      shape: BoxShape.circle,
                    ),
                    constraints: const BoxConstraints(minWidth: 18, minHeight: 18),
                    child: Text(
                      '$_unreadCount',
                      style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
            ],
          ),
          PopupMenuButton<int>(
            icon: const Icon(Icons.swap_horiz),
            tooltip: 'Cambiar dashboard',
            onSelected: (i) => setState(() => _currentIndex = i),
            itemBuilder: (_) => List.generate(_dashboards.length, (i) {
              final d = _dashboards[i];
              final id = d['id'] as String;
              return PopupMenuItem<int>(
                value: i,
                child: Row(
                  children: [
                    Icon(_dashboardIcons[id] ?? Icons.dashboard,
                         color: _currentIndex == i ? (_dashboardColors[id] ?? Colors.grey) : Colors.grey),
                    const SizedBox(width: 12),
                    Text(d['label'] ?? 'Dashboard',
                         style: TextStyle(fontWeight: _currentIndex == i ? FontWeight.bold : FontWeight.normal)),
                    if (_currentIndex == i) ...[
                      const Spacer(),
                      const Icon(Icons.check, size: 16, color: Colors.green),
                    ],
                  ],
                ),
              );
            }),
          ),
        ],
      ),
      drawer: _buildDrawer(),
      body: IndexedStack(
        index: _currentIndex,
        children: List.generate(_dashboards.length, (i) => _buildDashboard(i)),
      ),
    );
  }

  Widget _buildDrawer() {
    final user = widget.user;
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(color: Color(0xFF9b0b0b)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                CircleAvatar(
                  radius: 28,
                  backgroundColor: Colors.white,
                  child: Text(
                    user.name.isNotEmpty ? user.name[0].toUpperCase() : '?',
                    style: const TextStyle(fontSize: 24, color: Color(0xFF9b0b0b), fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(height: 8),
                Text(user.name, style: const TextStyle(color: Colors.white, fontSize: 16)),
                Text(user.email, style: const TextStyle(color: Colors.white70, fontSize: 13)),
                Text(user.roleName.toUpperCase(), style: const TextStyle(color: Colors.amber, fontSize: 11, fontWeight: FontWeight.bold)),
              ],
            ),
          ),
          ...List.generate(_dashboards.length, (i) {
            final d = _dashboards[i];
            final id = d['id'] as String;
            return ListTile(
              leading: Icon(_dashboardIcons[id] ?? Icons.dashboard,
                           color: _currentIndex == i ? (_dashboardColors[id] ?? Colors.orange) : null),
              title: Text(d['label'] ?? 'Dashboard'),
              selected: _currentIndex == i,
              selectedTileColor: Colors.orange.withValues(alpha: 0.1),
              onTap: () {
                setState(() => _currentIndex = i);
                Navigator.pop(context);
              },
            );
          }),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text('Cerrar sesión', style: TextStyle(color: Colors.red)),
            onTap: () async {
              await AuthService.logout();
              if (!context.mounted) return;
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                (_) => false,
              );
            },
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _notifTimer?.cancel();
    super.dispose();
  }
}
