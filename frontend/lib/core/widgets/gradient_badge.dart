import 'package:flutter/material.dart';

class GradientBadge extends StatelessWidget {
  const GradientBadge({super.key, required this.label});

  final String label;

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF4C6EF5), Color(0xFFA855F7)],
        ),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        child: Text(
          label.toUpperCase(),
          style: const TextStyle(
            color: Colors.white,
            letterSpacing: 0.6,
            fontSize: 12,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }
}
