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

  Future<void> _prepararPedido(int orderId) async {
    try {
      await _api.prepareOrder(orderId);
      await _loadData();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Pedido marcado como preparado')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  void _mostrarDialogEntrega(int orderId) {
    final descCtrl = TextEditingController();
    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Entregar Pedido'),
      content: TextField(
        controller: descCtrl,
        decoration: const InputDecoration(labelText: 'Notas de entrega'),
        maxLines: 3,
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () async {
            Navigator.pop(ctx);
            try {
              await _api.deliverOrder(orderId, description: descCtrl.text.isEmpty ? null : descCtrl.text);
              await _loadData();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Pedido entregado correctamente')),
              );
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
            }
          },
          child: const Text('Entregar'),
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
                      final status = p['status'] ?? 'pendiente';
                      final statusColor = status == 'entregado' ? Colors.grey
                          : status == 'preparado' ? Colors.blue : Colors.orange;
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Icon(Icons.receipt_long, color: statusColor, size: 28),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Text('Pedido #${p['id']} - ${p['profesor'] ?? 'Prof. #${p['user_id']}'}',
                                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15)),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 4),
                              Text('Estado: ${status[0].toUpperCase()}${status.substring(1)}',
                                style: TextStyle(color: statusColor, fontWeight: FontWeight.w500)),
                              ...items.map((item) => Text(
                                '  • ${item['category_name'] ?? 'Cat. #${item['category_id']}'} x${item['quantity']}',
                                style: const TextStyle(fontSize: 12, color: Colors.grey),
                              )),
                              const SizedBox(height: 8),
                              if (status == 'pendiente')
                                SizedBox(
                                  width: double.infinity,
                                  child: ElevatedButton.icon(
                                    icon: const Icon(Icons.check, size: 18),
                                    label: const Text('Preparar'),
                                    style: ElevatedButton.styleFrom(backgroundColor: Colors.orange, foregroundColor: Colors.white),
                                    onPressed: () => _prepararPedido(p['id']),
                                  ),
                                ),
                              if (status == 'preparado')
                                SizedBox(
                                  width: double.infinity,
                                  child: ElevatedButton.icon(
                                    icon: const Icon(Icons.handshake, size: 18),
                                    label: const Text('Entregar'),
                                    style: ElevatedButton.styleFrom(backgroundColor: Colors.blue, foregroundColor: Colors.white),
                                    onPressed: () => _mostrarDialogEntrega(p['id']),
                                  ),
                                ),
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
                      final catName = l['category_name'] ?? '?';
                      final userName = l['user_name'] ?? l['user_id'] ?? '?';
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  const Icon(Icons.bookmark, color: Colors.teal, size: 28),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(catName, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15)),
                                        Text('$userName  |  Cant: ${l['quantity'] ?? 1}',
                                          style: const TextStyle(color: Colors.grey, fontSize: 13)),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton.icon(
                                  icon: const Icon(Icons.reply, size: 18),
                                  label: const Text('Devolver'),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.teal,
                                    foregroundColor: Colors.white,
                                  ),
                                  onPressed: () => _mostrarDialogDevolver(l['id'] as int),
                                ),
                              ),
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

  void _mostrarDialogDevolver(int loanId) {
    final descCtrl = TextEditingController();
    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Devolver Préstamo'),
      content: TextField(
        controller: descCtrl,
        decoration: const InputDecoration(labelText: 'Notas de devolución'),
        maxLines: 3,
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () async {
            Navigator.pop(ctx);
            try {
              await _api.returnLoan(loanId, description: descCtrl.text.isEmpty ? null : descCtrl.text);
              await _loadData();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Préstamo devuelto correctamente')),
              );
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
            }
          },
          child: const Text('Devolver'),
        ),
      ],
    ));
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}
