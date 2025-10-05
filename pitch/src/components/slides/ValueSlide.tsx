import React from 'react';
import { Clock, DollarSign, Shield, TrendingUp } from 'lucide-react';

export const ValueSlide = () => (
  <div className="space-y-8">
    <h2 className="text-5xl font-bold text-white mb-8">Чому це важливо?</h2>
    <div className="grid grid-cols-2 gap-6">
      <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-8 border border-green-400/30">
        <Clock className="w-12 h-12 text-green-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-3">Швидше</h3>
        <p className="text-gray-300 text-lg mb-2">Time-to-market:</p>
        <div className="flex items-center gap-4">
          <span className="text-red-400 line-through text-xl">7-14 днів</span>
          <span className="text-4xl">→</span>
          <span className="text-green-400 font-bold text-2xl">2-4 години</span>
        </div>
      </div>
      <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl p-8 border border-blue-400/30">
        <DollarSign className="w-12 h-12 text-blue-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-3">Дешевше</h3>
        <p className="text-gray-300 text-lg mb-2">Cost per variation:</p>
        <div className="text-center mt-4">
          <div className="text-5xl font-bold text-blue-400">-70%</div>
          <p className="text-gray-400 mt-2">економія на виробництві</p>
        </div>
      </div>
      <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-8 border border-purple-400/30">
        <Shield className="w-12 h-12 text-purple-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-3">Безпечніше</h3>
        <p className="text-gray-300 text-lg mb-2">Рівень банів:</p>
        <div className="flex items-center gap-4">
          <span className="text-red-400 line-through text-xl">20-40%</span>
          <span className="text-4xl">→</span>
          <span className="text-green-400 font-bold text-2xl">&lt;5%</span>
        </div>
      </div>
      <div className="bg-gradient-to-br from-orange-500/20 to-yellow-500/20 rounded-xl p-8 border border-orange-400/30">
        <TrendingUp className="w-12 h-12 text-orange-400 mb-4" />
        <h3 className="text-3xl font-bold text-white mb-3">Масштабніше</h3>
        <p className="text-gray-300 text-lg mb-2">Продуктивність:</p>
        <div className="text-center mt-4">
          <div className="text-5xl font-bold text-orange-400">100+</div>
          <p className="text-gray-400 mt-2">варіацій на тиждень без росту команди</p>
        </div>
      </div>
    </div>
  </div>
);

export const valueSlideConfig = {
  title: "Цінність для бізнесу",
  bg: "bg-gradient-to-br from-green-900 via-emerald-900 to-teal-900"
};