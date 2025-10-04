import 'package:flutter/material.dart';

import '../analyze/analyze_screen.dart';
import '../check/check_screen.dart';
import '../create/create_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  static final List<_NavigationItem> _items = [
    _NavigationItem(
      label: 'Analyze',
      icon: Icons.analytics_outlined,
      selectedIcon: Icons.analytics,
      builder: (_) => const AnalyzeScreen(),
    ),
    _NavigationItem(
      label: 'Create',
      icon: Icons.auto_fix_high_outlined,
      selectedIcon: Icons.auto_fix_high,
      builder: (_) => const CreateScreen(),
    ),
    _NavigationItem(
      label: 'Check',
      icon: Icons.check_circle_outline,
      selectedIcon: Icons.check_circle,
      builder: (_) => const CheckScreen(),
    ),
  ];

  void _onDestinationSelected(int index) {
    setState(() => _selectedIndex = index);
  }

  Widget _buildContent(BuildContext context) {
    final item = _items[_selectedIndex];
    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 250),
      switchInCurve: Curves.easeOut,
      switchOutCurve: Curves.easeIn,
      child: KeyedSubtree(key: ValueKey(item.label), child: item.builder(context)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isWide = constraints.maxWidth >= 900;

        if (isWide) {
          return Scaffold(
            body: SafeArea(
              child: Row(
                children: [
                  NavigationRail(
                    selectedIndex: _selectedIndex,
                    onDestinationSelected: _onDestinationSelected,
                    labelType: NavigationRailLabelType.all,
                    destinations: [
                      for (final item in _items)
                        NavigationRailDestination(
                          icon: Icon(item.icon),
                          selectedIcon: Icon(item.selectedIcon),
                          label: Text(item.label),
                        ),
                    ],
                  ),
                  const VerticalDivider(width: 1),
                  Expanded(child: _buildContent(context)),
                ],
              ),
            ),
          );
        }

        return Scaffold(
          body: SafeArea(child: _buildContent(context)),
          bottomNavigationBar: NavigationBar(
            selectedIndex: _selectedIndex,
            onDestinationSelected: _onDestinationSelected,
            labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
            destinations: [
              for (final item in _items)
                NavigationDestination(
                  icon: Icon(item.icon),
                  selectedIcon: Icon(item.selectedIcon),
                  label: item.label,
                ),
            ],
          ),
        );
      },
    );
  }
}

class _NavigationItem {
  const _NavigationItem({
    required this.label,
    required this.icon,
    required this.selectedIcon,
    required this.builder,
  });

  final String label;
  final IconData icon;
  final IconData selectedIcon;
  final WidgetBuilder builder;
}
