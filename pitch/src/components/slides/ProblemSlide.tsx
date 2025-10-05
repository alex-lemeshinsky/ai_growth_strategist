import React from 'react';
import { Clock, DollarSign, AlertTriangle } from 'lucide-react';

export const ProblemSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-12">Креативне виробництво = найдорожча пляшка</h2>
    <div className="grid grid-cols-1 gap-6">
      <div className="bg-red-800/30 border-l-4 border-red-500 p-6 rounded-r-lg">
        <div className="flex items-start gap-4">
          <Clock className="w-8 h-8 text-red-400 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-2xl font-semibold text-white mb-2">Повільно</h3>
            <p className="text-gray-300 text-lg">Бриф → референси → сценарії → озвучка → монтаж → узгодження займає тижні</p>
          </div>
        </div>
      </div>
      <div className="bg-red-800/30 border-l-4 border-red-500 p-6 rounded-r-lg">
        <div className="flex items-start gap-4">
          <DollarSign className="w-8 h-8 text-red-400 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-2xl font-semibold text-white mb-2">Дорого</h3>
            <p className="text-gray-300 text-lg">Вартість однієї варіації: $500-2000. Масштабування потребує великої команди</p>
          </div>
        </div>
      </div>
      <div className="bg-red-800/30 border-l-4 border-red-500 p-6 rounded-r-lg">
        <div className="flex items-start gap-4">
          <AlertTriangle className="w-8 h-8 text-red-400 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-2xl font-semibold text-white mb-2">Ризиковано</h3>
            <p className="text-gray-300 text-lg">20-40% креативів отримують бани/попередження → втрата бюджету та часу</p>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export const problemSlideConfig = {
  title: "Проблема",
  bg: "bg-gradient-to-br from-red-900 to-gray-900"
};