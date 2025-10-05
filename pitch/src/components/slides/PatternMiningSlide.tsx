import React from 'react';
import { CheckCircle } from 'lucide-react';
import { AnalysisReportButton } from '../DemoButton';

export const PatternMiningSlide = () => (
  <div className="space-y-6">
    <div className="bg-blue-500/20 rounded-xl p-2 inline-block">
      <span className="text-blue-400 font-bold text-xl px-4">STEP 1</span>
    </div>
    <h2 className="text-5xl font-bold text-white">Pattern Mining з реальних кейсів</h2>
    <div className="grid grid-cols-2 gap-6 mt-8">
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-blue-500/30">
        <h3 className="text-2xl font-semibold text-blue-400 mb-4">Джерела</h3>
        <ul className="space-y-3 text-gray-300 text-lg">
          <li className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-400" />
            Meta Ad Library
          </li>
          <li className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-400" />
            TikTok Creative Center
          </li>
          <li className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-400" />
            Successful campaigns
          </li>
        </ul>
      </div>
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-purple-500/30">
        <h3 className="text-2xl font-semibold text-purple-400 mb-4">Аналіз</h3>
        <ul className="space-y-3 text-gray-300 text-lg">
          <li className="flex items-center gap-3">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            Hook структура
          </li>
          <li className="flex items-center gap-3">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            Емоційна дуга
          </li>
          <li className="flex items-center gap-3">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            CTA паттерни
          </li>
          <li className="flex items-center gap-3">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            Візуальний стиль
          </li>
        </ul>
      </div>
    </div>
    <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-6 border border-blue-400/30 mt-8">
      <div className="flex items-center justify-between">
        <p className="text-xl text-white font-semibold">
          💡 Результат: База паттернів з реальних, успішних оголошень — не випадкова генерація
        </p>
        <AnalysisReportButton 
          variant="secondary" 
          size="md" 
          showDescription={false}
        />
      </div>
    </div>
  </div>
);

export const patternMiningSlideConfig = {
  title: "Step 1: Pattern Mining",
  bg: "bg-gradient-to-br from-blue-900 to-indigo-900"
};