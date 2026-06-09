import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class AlumnoDashboard extends StatefulWidget {
  const AlumnoDashboard({super.key});
  @override
  State<AlumnoDashboard> createState() => _AlumnoDashboardState();
}

class _AlumnoDashboardState extends State<AlumnoDashboard> with SingleTickerProviderStateMixin {
  late ApiService _api;
  late TabController _tabController;

  List<dynamic> _tareas = [];
  List<dynamic> _materiales = [];
  List<dynamic> _documentos = [];
  List<dynamic> _compartidos = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
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
        _api.getTareas(),
        _api.getMateriales(),
        _api.getDocumentos(),
        _api.getCompartidos(),
      ]);
      _tareas = results[0];
      _materiales = results[1];
      _documentos = results[2];
      _compartidos = results[3];
      _loading = false;
      setState(() {});
    } catch (e) {
      _loading = false;
      _error = e.toString();
      setState(() {});
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
          labelColor: Colors.green,
          unselectedLabelColor: Colors.grey,
          indicatorColor: Colors.green,
          isScrollable: true,
          tabs: const [
            Tab(text: 'Tareas Pendientes'),
            Tab(text: 'Materiales'),
            Tab(text: 'Documentos'),
            Tab(text: 'Compartidos'),
          ],
        ),
        Expanded(
          child: TabBarView(
            controller: _tabController,
            children: [
              _buildTareasTab(),
              _buildListTab(_materiales, Icons.description, Colors.blue, 'No hay materiales disponibles'),
              _buildListTab(_documentos, Icons.article, Colors.purple, 'No hay documentos'),
              _buildListTab(_compartidos, Icons.share, Colors.green, 'No hay documentos compartidos'),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildTareasTab() {
    final pendientes = _tareas.where((t) => t['completada'] != true && t['estado'] != 'completada').toList();
    final entregadas = _tareas.where((t) => t['completada'] == true || t['estado'] == 'completada').toList();

    return RefreshIndicator(
      onRefresh: _loadData,
      child: ListView(
        children: [
          if (pendientes.isNotEmpty) ...[
            Padding(
              padding: const EdgeInsets.fromLTRB(12, 12, 12, 4),
              child: Row(
                children: [
                  Icon(Icons.pending, color: Colors.orange, size: 20),
                  const SizedBox(width: 6),
                  Text('Pendientes (${pendientes.length})', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            ...pendientes.map((t) => Card(
              margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              child: ListTile(
                leading: const Icon(Icons.pending, color: Colors.orange, size: 28),
                title: Text(t['titulo'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text(t['descripcion'] ?? 'Sin descripción'),
              ),
            )),
          ],
          if (entregadas.isNotEmpty) ...[
            Padding(
              padding: const EdgeInsets.fromLTRB(12, 16, 12, 4),
              child: Row(
                children: [
                  Icon(Icons.check_circle, color: Colors.green, size: 20),
                  const SizedBox(width: 6),
                  Text('Entregadas (${entregadas.length})', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            ...entregadas.map((t) => Card(
              margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              child: ListTile(
                leading: const Icon(Icons.check_circle, color: Colors.green, size: 28),
                title: Text(t['titulo'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text(t['descripcion'] ?? 'Sin descripción'),
              ),
            )),
          ],
          if (_tareas.isEmpty) const Center(child: Padding(
            padding: EdgeInsets.all(32),
            child: Text('No hay tareas disponibles'),
          )),
        ],
      ),
    );
  }

  Widget _buildListTab(List<dynamic> items, IconData icon, Color color, String emptyMsg) {
    return RefreshIndicator(
      onRefresh: _loadData,
      child: items.isEmpty
          ? Center(child: Text(emptyMsg))
          : ListView.builder(
              itemCount: items.length,
              itemBuilder: (_, i) {
                final item = items[i];
                final nombre = item['nombre'] ?? item['titulo'] ?? 'Elemento';
                final subt = item['url'] ?? item['archivo'] ?? item['descripcion'] ?? '';
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  child: ListTile(
                    leading: Icon(icon, color: color),
                    title: Text(nombre, style: const TextStyle(fontWeight: FontWeight.w600)),
                    subtitle: subt.isNotEmpty ? Text(subt) : null,
                  ),
                );
              },
            ),
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}
