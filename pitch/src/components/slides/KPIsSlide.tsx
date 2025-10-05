import React from 'react';
import { Clock, DollarSign, Shield, TrendingUp } from 'lucide-react';

export const KPIsSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Як вимірюємо успіх?</h2>
    <div className="grid grid-cols-2 gap-6">
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-emerald-400/30">
        <Clock className="w-12 h-12 text-emerald-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-2">Time-to-First-Creative</h3>
        <div className="text-5xl font-bold text-emerald-400 my-4">&lt; 30 хв</div>
        <p className="text-gray-300">Від брифу до першого креатива</p>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-teal-400/30">
        <DollarSign className="w-12 h-12 text-teal-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-2">Cost per Variation</h3>
        <div className="text-5xl font-bold text-teal-400 my-4">$5-15</div>
        <p className="text-gray-300">Замість $500-2000</p>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-green-400/30">
        <Shield className="w-12 h-12 text-green-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-2">Policy Pass Rate</h3>
        <div className="text-5xl font-bold text-green-400 my-4">&gt; 95%</div>
        <p className="text-gray-300">Креативів без банів/warnings</p>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-blue-400/30">
        <TrendingUp className="w-12 h-12 text-blue-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-2">Weekly Output</h3>
        <div className="text-5xl font-bold text-blue-400 my-4">100+</div>
        <p className="text-gray-300">Варіацій на команду з 2-3 людей</p>
      </div>
    </div>
  </div>
);

export const kpisSlideConfig = {
  title: "Метрики успіху",
  bg: "bg-gradient-to-br from-emerald-900 to-teal-900"
};