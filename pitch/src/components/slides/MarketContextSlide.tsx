import React from 'react';
import { Target, TrendingUp } from 'lucide-react';

export const MarketContextSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Чому Universe Group?</h2>
    <div className="grid grid-cols-2 gap-6">
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-yellow-400/30">
        <h3 className="text-2xl font-semibold text-yellow-400 mb-4">Досвід масштабування</h3>
        <div className="space-y-3 text-gray-300">
          <p className="text-lg"><span className="font-bold text-white">200M+</span> користувачів</p>
          <p className="text-lg"><span className="font-bold text-white">180</span> країн світу</p>
          <p className="text-lg"><span className="font-bold text-white">3200+</span> людей у команді</p>
        </div>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-orange-400/30">
        <h3 className="text-2xl font-semibold text-orange-400 mb-4">Успішні продукти</h3>
        <div className="space-y-2 text-gray-300">
          <p>Cleaner Guru: 27M+ downloads</p>
          <p>Scan Guru: 35M+ downloads</p>
          <p>Visify: 2.5M downloads, 5M+ AI generations</p>
        </div>
      </div>
    </div>
    <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-8 border border-blue-400/30 mt-8">
      <h3 className="text-3xl font-bold text-white mb-4">Чому це важливо для вас?</h3>
      <div className="grid grid-cols-2 gap-6 text-lg text-gray-300">
        <div>
          <Target className="w-8 h-8 text-blue-400 mb-2" />
          <p>Витрачаємо мільйони $ на рекламу</p>
          <p className="text-sm text-gray-400 mt-1">Креативи = критичний bottleneck</p>
        </div>
        <div>
          <TrendingUp className="w-8 h-8 text-purple-400 mb-2" />
          <p>Потрібно 100+ варіацій/тиждень</p>
          <p className="text-sm text-gray-400 mt-1">Поточна команда не масштабується</p>
        </div>
      </div>
    </div>
  </div>
);

export const marketContextSlideConfig = {
  title: "Universe Group Context",
  bg: "bg-gradient-to-br from-yellow-900 via-orange-900 to-red-900"
};