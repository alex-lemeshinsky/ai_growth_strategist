import React from 'react';
import { CheckCircle } from 'lucide-react';

export const NextStepsSlide = () => (
  <div className="space-y-8">
    <h2 className="text-6xl font-bold text-white mb-12 text-center">Готові до запуску!</h2>
    <div className="grid grid-cols-3 gap-6">
      <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-8 border border-green-400/30 text-center">
        <div className="text-6xl mb-4">✅</div>
        <h3 className="text-2xl font-bold text-white mb-3">70% готово</h3>
        <p className="text-gray-300">Pattern Mining, Chat MVP Pro, Policy Checker працюють</p>
      </div>
      <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl p-8 border border-blue-400/30 text-center">
        <div className="text-6xl mb-4">⚡</div>
        <h3 className="text-2xl font-bold text-white mb-3">2-4 тижні</h3>
        <p className="text-gray-300">До повного MVP з video generation</p>
      </div>
      <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-8 border border-purple-400/30 text-center">
        <div className="text-6xl mb-4">🚀</div>
        <h3 className="text-2xl font-bold text-white mb-3">Ready for pilot</h3>
        <p className="text-gray-300">Пошук партнера для тестування</p>
      </div>
    </div>
    <div className="bg-gradient-to-r from-yellow-500/30 to-orange-500/30 rounded-2xl p-10 border-2 border-yellow-400/50 mt-12">
      <h3 className="text-3xl font-bold text-white mb-6 text-center">Потребуємо:</h3>
      <div className="grid grid-cols-2 gap-6 text-lg text-gray-200">
        <div className="flex items-start gap-3">
          <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
          <span>Доступ до тестових ассетів і прикладів</span>
        </div>
        <div className="flex items-start gap-3">
          <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
          <span>Інфраструктура S3/GCS для зберігання</span>
        </div>
        <div className="flex items-start gap-3">
          <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
          <span>Партнер для пілоту (агентство/бренд)</span>
        </div>
        <div className="flex items-start gap-3">
          <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
          <span>Feedback від performance команд</span>
        </div>
      </div>
    </div>
  </div>
);

export const nextStepsSlideConfig = {
  title: "Наступні кроки",
  bg: "bg-gradient-to-br from-purple-900 via-pink-900 to-red-900"
};