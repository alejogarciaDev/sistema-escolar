import 'dart:io';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:file_picker/file_picker.dart';
import '../services/api_service.dart';

class OficinaAlumnosDashboard extends StatefulWidget {
  const OficinaAlumnosDashboard({super.key});
  @override
  State<OficinaAlumnosDashboard> createState() => _OficinaAlumnosDashboardState();
}

class _OficinaAlumnosDashboardState extends State<OficinaAlumnosDashboard> {
  late ApiService _api;
  final _dniCtrl = TextEditingController();

  Map<String, dynamic>? _alumno;
  List<dynamic> _historial = [];
  bool _searching = false;
  bool _loadingHistorial = false;
  String? _searchError;

  final _nombreCtrl = TextEditingController();
  final _folioCtrl = TextEditingController();
  final _legajoCtrl = TextEditingController();
  final _direccionCtrl = TextEditingController();
  final _telefonoCtrl = TextEditingController();
  bool _editing = false;

  // Historial fields
  final _anioCtrl = TextEditingController();
  final _materiaCtrl = TextEditingController();
  final _notaCtrl = TextEditingController();
  final _estadoCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token') ?? '';
    _api = ApiService(token);
  }

  Future<void> _searchAlumno() async {
    final dni = _dniCtrl.text.trim();
    if (dni.isEmpty) return;
    setState(() { _searching = true; _searchError = null; _alumno = null; _historial = []; });
    try {
      _alumno = await _api.getAlumnoByDni(dni);
      _nombreCtrl.text = _alumno!['nombre'] ?? '';
      _folioCtrl.text = (_alumno!['folio'] ?? '').toString();
      _legajoCtrl.text = (_alumno!['legajo'] ?? '').toString();
      _direccionCtrl.text = _alumno!['direccion'] ?? '';
      _telefonoCtrl.text = _alumno!['telefono'] ?? '';
      _editing = false;
      await _loadHistorial();
    } catch (e) {
      _searchError = 'Alumno no encontrado';
    }
    setState(() { _searching = false; });
  }

  Future<void> _loadHistorial() async {
    final dni = _dniCtrl.text.trim();
    if (dni.isEmpty) return;
    try {
      _loadingHistorial = true;
      setState(() {});
      _historial = await _api.getHistorial(dni);
      _loadingHistorial = false;
      setState(() {});
    } catch (e) {
      _loadingHistorial = false;
      setState(() {});
    }
  }

  Future<void> _saveAlumno() async {
    final dni = _dniCtrl.text.trim();
    try {
      await _api.updateAlumno(dni, {
        'nombre': _nombreCtrl.text,
        'folio': _folioCtrl.text,
        'legajo': _legajoCtrl.text,
        'direccion': _direccionCtrl.text,
        'telefono': _telefonoCtrl.text,
      });
      _alumno = await _api.getAlumnoByDni(dni);
      _editing = false;
      setState(() {});
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Alumno actualizado')));
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  Future<void> _addHistorial() async {
    final dni = _dniCtrl.text.trim();
    try {
      await _api.addHistorial(dni, {
        'anio': _anioCtrl.text,
        'materia': _materiaCtrl.text,
        'nota': _notaCtrl.text,
        'estado': _estadoCtrl.text,
      });
      _anioCtrl.clear();
      _materiaCtrl.clear();
      _notaCtrl.clear();
      _estadoCtrl.clear();
      await _loadHistorial();
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Historial agregado')));
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  Future<void> _deleteHistorial(int id) async {
    try {
      await _api.deleteHistorial(id);
      await _loadHistorial();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  Future<void> _uploadFile() async {
    final result = await FilePicker.platform.pickFiles();
    if (result == null || result.files.single.path == null) return;
    final dni = _dniCtrl.text.trim();
    try {
      await _api.uploadFile(dni, result.files.single.path!);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Archivo subido')));
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Oficina Alumnos', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _dniCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Buscar por DNI',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.search),
                  ),
                  keyboardType: TextInputType.number,
                ),
              ),
              const SizedBox(width: 8),
              ElevatedButton(
                onPressed: _searching ? null : _searchAlumno,
                child: _searching ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) : const Text('Buscar'),
              ),
            ],
          ),
          if (_searchError != null) Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Text(_searchError!, style: const TextStyle(color: Colors.red, fontSize: 16)),
          ),
          if (_alumno != null) ...[
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.person, color: Colors.purple),
                        const SizedBox(width: 8),
                        const Text('Datos del Alumno', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                        const Spacer(),
                        IconButton(
                          icon: Icon(_editing ? Icons.close : Icons.edit, color: Colors.purple),
                          onPressed: () => setState(() => _editing = !_editing),
                        ),
                      ],
                    ),
                    const Divider(),
                    if (_editing) ...[
                      TextField(controller: _nombreCtrl, decoration: const InputDecoration(labelText: 'Nombre')),
                      TextField(controller: _folioCtrl, decoration: const InputDecoration(labelText: 'Folio')),
                      TextField(controller: _legajoCtrl, decoration: const InputDecoration(labelText: 'Legajo')),
                      TextField(controller: _direccionCtrl, decoration: const InputDecoration(labelText: 'Dirección')),
                      TextField(controller: _telefonoCtrl, decoration: const InputDecoration(labelText: 'Teléfono')),
                      const SizedBox(height: 12),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.save),
                        label: const Text('Guardar Cambios'),
                        onPressed: _saveAlumno,
                      ),
                    ] else ...[
                      _dataRow('Nombre', _alumno!['nombre'] ?? ''),
                      _dataRow('DNI', _alumno!['dni'] ?? ''),
                      _dataRow('Folio', (_alumno!['folio'] ?? '').toString()),
                      _dataRow('Legajo', (_alumno!['legajo'] ?? '').toString()),
                      _dataRow('Dirección', _alumno!['direccion'] ?? ''),
                      _dataRow('Teléfono', _alumno!['telefono'] ?? ''),
                    ],
                  ],
                ),
              ),
            ),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              icon: const Icon(Icons.upload_file),
              label: const Text('Subir Archivo'),
              onPressed: _uploadFile,
            ),
            const SizedBox(height: 16),
            const Text('Historial Académico', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            if (_loadingHistorial)
              const Center(child: CircularProgressIndicator())
            else
              ..._historial.map((h) => Card(
                margin: const EdgeInsets.symmetric(vertical: 4),
                child: ListTile(
                  leading: const Icon(Icons.school, color: Colors.purple),
                  title: Text('${h['materia'] ?? ''} - ${h['anio'] ?? ''}'),
                  subtitle: Text('Nota: ${h['nota'] ?? '-'} | Estado: ${h['estado'] ?? '-'}'),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete, color: Colors.red),
                    onPressed: () => _deleteHistorial(h['id']),
                  ),
                ),
              )),
            const SizedBox(height: 12),
            const Text('Agregar al Historial', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(child: TextField(controller: _anioCtrl, decoration: const InputDecoration(labelText: 'Año', border: OutlineInputBorder()), keyboardType: TextInputType.number)),
                const SizedBox(width: 8),
                Expanded(child: TextField(controller: _materiaCtrl, decoration: const InputDecoration(labelText: 'Materia', border: OutlineInputBorder()))),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(child: TextField(controller: _notaCtrl, decoration: const InputDecoration(labelText: 'Nota', border: OutlineInputBorder()))),
                const SizedBox(width: 8),
                Expanded(child: TextField(controller: _estadoCtrl, decoration: const InputDecoration(labelText: 'Estado', border: OutlineInputBorder()))),
              ],
            ),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              icon: const Icon(Icons.add),
              label: const Text('Agregar'),
              onPressed: _addHistorial,
            ),
          ],
        ],
      ),
    );
  }

  Widget _dataRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          SizedBox(width: 100, child: Text('$label:', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.grey))),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _dniCtrl.dispose();
    _nombreCtrl.dispose();
    _folioCtrl.dispose();
    _legajoCtrl.dispose();
    _direccionCtrl.dispose();
    _telefonoCtrl.dispose();
    _anioCtrl.dispose();
    _materiaCtrl.dispose();
    _notaCtrl.dispose();
    _estadoCtrl.dispose();
    super.dispose();
  }
}
