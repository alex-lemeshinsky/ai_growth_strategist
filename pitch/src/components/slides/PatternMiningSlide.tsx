import React from 'react';
import { CheckCircle, ArrowRight } from 'lucide-react';
import { AnalysisReportButton, ChatDemoButton } from '../DemoButton';

export const PatternMiningSlide = () => (
  <div className="space-y-6">
    <div className="bg-gradient-to-r from-blue-500/20 to-orange-500/20 rounded-xl p-3 inline-block border border-blue-400/30">
      <span className="text-blue-300 font-bold text-xl px-4">STEP 1: АНАЛІЗ</span>
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
    {/* Result format */}
    <div className="bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-xl p-6 border border-orange-400/30 mt-8">
      <h3 className="text-xl font-bold text-orange-300 mb-4">📊 Новий структурований формат результату:</h3>
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-lg font-semibold text-orange-300">Pain_points</div>
          <div className="text-xs text-gray-400 mt-1">Болі аудиторії</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-lg font-semibold text-blue-300">Visual_trends</div>
          <div className="text-xs text-gray-400 mt-1">Кольори, фільтри</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-lg font-semibold text-green-300">Hooks</div>
          <div className="text-xs text-gray-400 mt-1">Популярні хуки</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-lg font-semibold text-purple-300">Concept</div>
          <div className="text-xs text-gray-400 mt-1">Концепції</div>
        </div>
      </div>
      <div className="flex items-center justify-between">
        <p className="text-lg text-white font-medium">
          💡 Структуровані дані для персоналізованого чату
        </p>
        <AnalysisReportButton 
          variant="secondary" 
          size="md" 
          showDescription={false}
        />
      </div>
    </div>

    {/* Demo flow */}
    <div className="bg-gradient-to-r from-green-500/20 to-blue-500/20 rounded-xl p-6 border border-green-400/30 mt-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-6">
          <div className="text-center">
            <div className="text-lg font-semibold text-green-300">📊 Аналіз</div>
            <div className="text-sm text-gray-400">Завершено</div>
          </div>
          <ArrowRight className="w-6 h-6 text-gray-400" />
          <div className="text-center">
            <div className="text-lg font-semibold text-blue-300">💬 Чат</div>
            <div className="text-sm text-gray-400">Демо</div>
          </div>
        </div>
        <ChatDemoButton 
          variant="primary" 
          size="lg" 
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