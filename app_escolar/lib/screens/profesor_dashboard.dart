import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class ProfesorDashboard extends StatefulWidget {
  const ProfesorDashboard({super.key});
  @override
  State<ProfesorDashboard> createState() => _ProfesorDashboardState();
}

class _ProfesorDashboardState extends State<ProfesorDashboard> with SingleTickerProviderStateMixin {
  late ApiService _api;
  late TabController _tabController;

  List<dynamic> _tareas = [];
  List<dynamic> _materiales = [];
  List<dynamic> _compartidos = [];
  List<dynamic> _pedidos = [];
  List<dynamic> _categorias = [];
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
        _api.getCompartidos(),
        _api.getMyPedidos(),
        _api.getCategorias(),
      ]);
      _tareas = results[0];
      _materiales = results[1];
      _compartidos = results[2];
      _pedidos = results[3];
      _categorias = results[4];
      _loading = false;
      setState(() {});
    } catch (e) {
      _loading = false;
      _error = e.toString();
      setState(() {});
    }
  }

  void _showCreateTareaDialog() {
    final tituloCtrl = TextEditingController();
    final descCtrl = TextEditingController();

    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Nueva Tarea'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: tituloCtrl, decoration: const InputDecoration(labelText: 'Título')),
          TextField(controller: descCtrl, decoration: const InputDecoration(labelText: 'Descripción'), maxLines: 3),
        ],
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () async {
            if (tituloCtrl.text.isEmpty) return;
            try {
              await _api.createTarea({'titulo': tituloCtrl.text, 'descripcion': descCtrl.text});
              Navigator.pop(ctx);
              await _loadData();
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
            }
          },
          child: const Text('Crear'),
        ),
      ],
    ));
  }

  void _showCreatePedidoDialog() {
    if (_categorias.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No hay categorías disponibles en el Pañol')),
      );
      return;
    }
    final qtyCtrl = TextEditingController(text: '1');
    int? selectedCatId;
    String? selectedCatName;

    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Nuevo Pedido al Pañol'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          DropdownButtonFormField<int>(
            decoration: const InputDecoration(labelText: 'Categoría'),
            items: _categorias.map((c) => DropdownMenuItem<int>(
              value: c['id'] as int,
              child: Text('${c['name']} (stock: ${c['stock'] ?? 0})'),
            )).toList(),
            onChanged: (v) { selectedCatId = v; selectedCatName = _categorias.firstWhere((c) => c['id'] == v)['name'] as String; },
          ),
          const SizedBox(height: 12),
          TextField(controller: qtyCtrl, decoration: const InputDecoration(labelText: 'Cantidad'), keyboardType: TextInputType.number),
        ],
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () async {
            if (selectedCatId == null) return;
            final qty = int.tryParse(qtyCtrl.text) ?? 1;
            if (qty <= 0) return;
            try {
              await _api.createPedido({'items': [{'category_id': selectedCatId, 'quantity': qty}]});
              Navigator.pop(ctx);
              await _loadData();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Pedido creado: $selectedCatName x$qty')),
              );
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
            }
          },
          child: const Text('Pedir'),
        ),
      ],
    ));
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_error != null) return Center(child: Text('Error: $_error'));

    return Column(
      children: [
        TabBar(
          controller: _tabController,
          labelColor: Colors.blue,
          unselectedLabelColor: Colors.grey,
          indicatorColor: Colors.blue,
          isScrollable: true,
          tabs: const [
            Tab(text: 'Tareas'),
            Tab(text: 'Materiales'),
            Tab(text: 'Compartidos'),
            Tab(text: 'Pedidos Pañol'),
          ],
        ),
        Expanded(
          child: TabBarView(
            controller: _tabController,
            children: [
              _buildTareasTab(),
              _buildMaterialesTab(),
              _buildCompartidosTab(),
              _buildPedidosTab(),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildTareasTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Todas las Tareas', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              ElevatedButton.icon(
                icon: const Icon(Icons.add),
                label: const Text('Nueva'),
                onPressed: _showCreateTareaDialog,
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: ListView.builder(
              itemCount: _tareas.length,
              itemBuilder: (_, i) {
                final t = _tareas[i];
                final completa = t['completada'] == true || t['estado'] == 'completada';
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  child: ListTile(
                    leading: Icon(
                      completa ? Icons.check_circle : Icons.pending,
                      color: completa ? Colors.green : Colors.orange,
                      size: 32,
                    ),
                    title: Text(t['titulo'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                    subtitle: Text(t['descripcion'] ?? 'Sin descripción'),
                    trailing: Text(completa ? 'Completada' : 'Pendiente', style: TextStyle(
                      color: completa ? Colors.green : Colors.orange,
                      fontSize: 12,
                    )),
                  ),
                );
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildMaterialesTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Materiales de Estudio', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              IconButton(
                icon: const Icon(Icons.refresh),
                onPressed: _loadData,
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: _materiales.isEmpty
                ? const Center(child: Text('No hay materiales disponibles'))
                : ListView.builder(
                    itemCount: _materiales.length,
                    itemBuilder: (_, i) {
                      final m = _materiales[i];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: ListTile(
                          leading: const Icon(Icons.description, color: Colors.blue),
                          title: Text(m['nombre'] ?? m['titulo'] ?? 'Material'),
                          subtitle: Text(m['url'] ?? m['archivo'] ?? ''),
                        ),
                      );
                    },
                  ),
          ),
        ),
      ],
    );
  }

  Widget _buildCompartidosTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Documentos Compartidos', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              IconButton(
                icon: const Icon(Icons.refresh),
                onPressed: _loadData,
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: _compartidos.isEmpty
                ? const Center(child: Text('No hay documentos compartidos'))
                : ListView.builder(
                    itemCount: _compartidos.length,
                    itemBuilder: (_, i) {
                      final c = _compartidos[i];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: ListTile(
                          leading: const Icon(Icons.share, color: Colors.green),
                          title: Text(c['nombre'] ?? c['titulo'] ?? 'Documento'),
                          subtitle: Text('Subido por: ${c['usuario'] ?? c['user_id'] ?? '?'}'),
                        ),
                      );
                    },
                  ),
          ),
        ),
      ],
    );
  }

  Widget _buildPedidosTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Mis Pedidos al Pañol', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              ElevatedButton.icon(
                icon: const Icon(Icons.add),
                label: const Text('Nuevo'),
                onPressed: _showCreatePedidoDialog,
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: _pedidos.isEmpty
                ? const Center(child: Text('No tienes pedidos'))
                : ListView.builder(
                    itemCount: _pedidos.length,
                    itemBuilder: (_, i) {
                      final p = _pedidos[i];
                      final items = p['items'] as List<dynamic>? ?? [];
                      final status = p['status'] ?? 'pendiente';
                      final statusColor = status == 'entregado' ? Colors.green
                          : status == 'preparado' ? Colors.blue : Colors.orange;
                      final statusIcon = status == 'entregado' ? Icons.check_circle
                          : status == 'preparado' ? Icons.inventory : Icons.pending;
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: ListTile(
                          leading: Icon(statusIcon, color: statusColor, size: 32),
                          title: Text('Pedido #${p['id']}', style: const TextStyle(fontWeight: FontWeight.w600)),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Estado: ${status[0].toUpperCase()}${status.substring(1)}',
                                style: TextStyle(color: statusColor, fontWeight: FontWeight.w500)),
                              ...items.map((item) => Text(
                                '  • ${item['category_name'] ?? 'Cat. #${item['category_id']}'} x${item['quantity']}',
                                style: const TextStyle(fontSize: 12),
                              )),
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

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}
