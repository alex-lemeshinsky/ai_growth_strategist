import React from 'react';

export const GoToMarketSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Стратегія виходу на ринок</h2>
    <div className="grid grid-cols-2 gap-6">
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-cyan-400/30">
        <h3 className="text-2xl font-semibold text-cyan-400 mb-4">Цільова аудиторія</h3>
        <ul className="space-y-3 text-gray-300 text-lg">
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
            <span>Performance marketing teams у продуктових компаніях</span>
          </li>
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
            <span>Digital marketing агентства</span>
          </li>
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
            <span>DTC бренди з high-volume UA</span>
          </li>
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
            <span>Mobile app developers</span>
          </li>
        </ul>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-blue-400/30">
        <h3 className="text-2xl font-semibold text-blue-400 mb-4">Ціноутворення</h3>
        <div className="space-y-4 text-gray-300">
          <div className="bg-blue-500/20 p-4 rounded-lg">
            <p className="font-semibold text-white mb-1">Starter</p>
            <p className="text-2xl font-bold text-blue-400">$299/міс</p>
            <p className="text-sm">50 креативів, базовий policy check</p>
          </div>
          <div className="bg-blue-500/30 p-4 rounded-lg border border-blue-400">
            <p className="font-semibold text-white mb-1">Pro</p>
            <p className="text-2xl font-bold text-blue-400">$999/міс</p>
            <p className="text-sm">500 креативів, advanced analytics</p>
          </div>
          <div className="bg-blue-500/20 p-4 rounded-lg">
            <p className="font-semibold text-white mb-1">Enterprise</p>
            <p className="text-2xl font-bold text-blue-400">Custom</p>
            <p className="text-sm">Unlimited, API access, dedicated support</p>
          </div>
        </div>
      </div>
    </div>
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-green-400/30 mt-6">
      <h3 className="text-2xl font-semibold text-green-400 mb-4">Канали</h3>
      <div className="grid grid-cols-3 gap-4 text-gray-300">
        <div className="text-center p-4 bg-green-500/20 rounded-lg">
          <p className="font-semibold text-white">Партнерства</p>
          <p className="text-sm mt-2">З агентствами та UA networks</p>
        </div>
        <div className="text-center p-4 bg-green-500/20 rounded-lg">
          <p className="font-semibold text-white">Спільноти</p>
          <p className="text-sm mt-2">Performance marketing groups</p>
        </div>
        <div className="text-center p-4 bg-green-500/20 rounded-lg">
          <p className="font-semibold text-white">Інтеграції</p>
          <p className="text-sm mt-2">Meta, TikTok, Google Ads</p>
        </div>
      </div>
    </div>
  </div>
);

export const goToMarketSlideConfig = {
  title: "Go-to-Market",
  bg: "bg-gradient-to-br from-cyan-900 to-blue-900"
};