import 'package:flutter/material.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import 'login_screen.dart';
import 'admin_dashboard.dart';
import 'profesor_dashboard.dart';
import 'alumno_dashboard.dart';
import 'panol_dashboard.dart';
import 'oficina_dashboard.dart';

class HomeScreen extends StatelessWidget {
  final User user;

  const HomeScreen({super.key, required this.user});

  @override
  Widget build(BuildContext context) {
    if (user.isAdmin) return const AdminDashboard();
    if (user.isProfesor) return const ProfesorDashboard();
    if (user.isAlumno) return const AlumnoDashboard();
    if (user.isPanol) return const PanolDashboard();
    if (user.isOficinaAlumnos) return const OficinaAlumnosDashboard();
    return const AlumnoDashboard();
  }
}

class DrawerMenu extends StatelessWidget {
  final User user;

  const DrawerMenu({super.key, required this.user});

  @override
  Widget build(BuildContext context) {
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
                    user.name.isNotEmpty
                        ? user.name[0].toUpperCase()
                        : '?',
                    style: const TextStyle(
                      fontSize: 24,
                      color: Color(0xFF9b0b0b),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  user.name,
                  style: const TextStyle(color: Colors.white, fontSize: 16),
                ),
                Text(
                  user.email,
                  style: const TextStyle(color: Colors.white70, fontSize: 13),
                ),
                Text(
                  user.roleName.toUpperCase(),
                  style: const TextStyle(
                    color: Colors.amber,
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          ListTile(
            leading: const Icon(Icons.dashboard),
            title: const Text('Dashboard'),
            onTap: () => Navigator.pop(context),
          ),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text('Cerrar sesi�n', style: TextStyle(color: Colors.red)),
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
}
