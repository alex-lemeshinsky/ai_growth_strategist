import React from 'react';

export const AdvantagesSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Чим відрізняємось від конкурентів?</h2>
    <div className="space-y-4">
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-blue-500">
        <h3 className="text-2xl font-semibold text-blue-400 mb-2">🎯 Патерни з реальних оголошень</h3>
        <p className="text-gray-300 text-lg">Не абстрактна генерація — база успішних кейсів з Meta Ad Library, TikTok Creative Center</p>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-purple-500">
        <h3 className="text-2xl font-semibold text-purple-400 mb-2">🧠 Deep Analysis</h3>
        <p className="text-gray-300 text-lg">Психологічні тригери, емоційна дуга, гіпотези для A/B тестування</p>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-green-500">
        <h3 className="text-2xl font-semibold text-green-400 mb-2">🛡️ Comprehensive Policy Check</h3>
        <p className="text-gray-300 text-lg">Не просто детекція — конкретні action items і автоматичні фікси</p>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-orange-500">
        <h3 className="text-2xl font-semibold text-orange-400 mb-2">🔄 Fix-it Chain</h3>
        <p className="text-gray-300 text-lg">Від виявлення ризику → переписаний VO/саби → автоматичний re-render</p>
      </div>
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-pink-500">
        <h3 className="text-2xl font-semibold text-pink-400 mb-2">📱 Platform-Native</h3>
        <p className="text-gray-300 text-lg">Автоматична адаптація форматів, шрифтів, CTA під кожну платформу</p>
      </div>
    </div>
  </div>
);

export const advantagesSlideConfig = {
  title: "Унікальні переваги",
  bg: "bg-gradient-to-br from-indigo-900 to-purple-900"
};