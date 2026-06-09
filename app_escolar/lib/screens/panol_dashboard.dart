import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class PanolDashboard extends StatefulWidget {
  const PanolDashboard({super.key});
  @override
  State<PanolDashboard> createState() => _PanolDashboardState();
}

class _PanolDashboardState extends State<PanolDashboard> with SingleTickerProviderStateMixin {
  late ApiService _api;
  late TabController _tabController;

  List<dynamic> _categorias = [];
  List<dynamic> _pedidos = [];
  List<dynamic> _prestamos = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
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
        _api.getCategorias(),
        _api.getPedidos(),
        _api.getPrestamos(),
      ]);
      _categorias = results[0];
      _pedidos = results[1];
      _prestamos = results[2];
      _loading = false;
      setState(() {});
    } catch (e) {
      _loading = false;
      _error = e.toString();
      setState(() {});
    }
  }

  void _showCreateCategoriaDialog() {
    final nameCtrl = TextEditingController();
    final barcodeCtrl = TextEditingController();
    final stockCtrl = TextEditingController(text: '0');

    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Nueva Categoría'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Nombre')),
          TextField(controller: barcodeCtrl, decoration: const InputDecoration(labelText: 'Código de barras')),
          TextField(controller: stockCtrl, decoration: const InputDecoration(labelText: 'Stock inicial'), keyboardType: TextInputType.number),
        ],
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () async {
            if (nameCtrl.text.isEmpty) return;
            try {
              await _api.createCategoria({
                'name': nameCtrl.text,
                'barcode': barcodeCtrl.text.isEmpty ? null : barcodeCtrl.text,
                'stock': int.tryParse(stockCtrl.text) ?? 0,
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
          labelColor: Colors.orange,
          unselectedLabelColor: Colors.grey,
          indicatorColor: Colors.orange,
          tabs: const [
            Tab(text: 'Categorías'),
            Tab(text: 'Pedidos'),
            Tab(text: 'Préstamos'),
          ],
        ),
        Expanded(
          child: TabBarView(
            controller: _tabController,
            children: [
              _buildCategoriasTab(),
              _buildPedidosTab(),
              _buildPrestamosTab(),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildCategoriasTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Inventario', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              ElevatedButton.icon(
                icon: const Icon(Icons.add),
                label: const Text('Nueva'),
                onPressed: _showCreateCategoriaDialog,
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: _categorias.isEmpty
                ? const Center(child: Text('No hay categorías'))
                : ListView.builder(
                    itemCount: _categorias.length,
                    itemBuilder: (_, i) {
                      final c = _categorias[i];
                      final stock = c['stock'] ?? 0;
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: stock > 0 ? Colors.green.shade100 : Colors.red.shade100,
                            child: Icon(Icons.inventory_2, color: stock > 0 ? Colors.green : Colors.red),
                          ),
                          title: Text(c['name'] ?? 'Categoría', style: const TextStyle(fontWeight: FontWeight.w600)),
                          subtitle: Text('Stock: $stock${c['barcode'] != null ? '  |  Código: ${c['barcode']}' : ''}'),
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
              const Text('Pedidos Pendientes', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              IconButton(icon: const Icon(Icons.refresh), onPressed: _loadData),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: _pedidos.isEmpty
                ? const Center(child: Text('No hay pedidos pendientes'))
                : ListView.builder(
                    itemCount: _pedidos.length,
                    itemBuilder: (_, i) {
                      final p = _pedidos[i];
                      final items = p['items'] as List<dynamic>? ?? [];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: ListTile(
                          leading: const Icon(Icons.receipt_long, color: Colors.orange),
                          title: Text('Pedido #${p['id']}', style: const TextStyle(fontWeight: FontWeight.w600)),
                          subtitle: Text('Profesor: ${p['profesor'] ?? p['user_id'] ?? '?'}  |  Estado: ${p['status'] ?? 'pendiente'}  |  Items: ${items.length}'),
                        ),
                      );
                    },
                  ),
          ),
        ),
      ],
    );
  }

  Widget _buildPrestamosTab() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Text('Préstamos Activos', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              IconButton(icon: const Icon(Icons.refresh), onPressed: _loadData),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: _loadData,
            child: _prestamos.isEmpty
                ? const Center(child: Text('No hay préstamos activos'))
                : ListView.builder(
                    itemCount: _prestamos.length,
                    itemBuilder: (_, i) {
                      final l = _prestamos[i];
                      final catName = l['category_name'] ?? l['category']?['name'] ?? '?';
                      final userName = l['user_name'] ?? l['user']?['name'] ?? l['user_id'] ?? '?';
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: ListTile(
                          leading: const Icon(Icons.bookmark, color: Colors.teal),
                          title: Text(catName, style: const TextStyle(fontWeight: FontWeight.w600)),
                          subtitle: Text('Usuario: $userName  |  Cant: ${l['quantity'] ?? 1}'),
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
