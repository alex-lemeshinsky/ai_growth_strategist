import React from 'react';
import { Play, ExternalLink } from 'lucide-react';
import { 
  AnalysisReportButton, 
  ChatDemoButton, 
  PolicyReportButton, 
  ApiDocsButton 
} from '../DemoButton';

export const LiveDemoSlide = () => (
  <div className="space-y-8">
    <h2 className="text-5xl font-bold text-white mb-8 text-center">🚀 Живі демо</h2>
    
    <div className="grid grid-cols-2 gap-8">
      {/* Step 1 Demo */}
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-blue-500/30">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-blue-500/20 rounded-lg px-3 py-1">
            <span className="text-blue-400 font-bold">STEP 1</span>
          </div>
        </div>
        <h3 className="text-2xl font-semibold text-blue-400 mb-3">Pattern Mining</h3>
        <p className="text-gray-300 mb-6">
          Інтерактивний звіт з аналізу конкурентів, стратегіями та інсайтами з реальних Meta Ads
        </p>
        <AnalysisReportButton 
          variant="primary" 
          size="lg" 
          showDescription={false}
        />
      </div>

      {/* Step 2 Demo */}
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-purple-500/30">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-purple-500/20 rounded-lg px-3 py-1">
            <span className="text-purple-400 font-bold">STEP 2</span>
          </div>
        </div>
        <h3 className="text-2xl font-semibold text-purple-400 mb-3">Chat MVP Pro</h3>
        <p className="text-gray-300 mb-6">
          Живий чат для збору брифу з персоналізованими рекомендаціями на основі аналізу конкурентів
        </p>
        <ChatDemoButton 
          variant="primary" 
          size="lg" 
          showDescription={false}
        />
      </div>

      {/* Step 3 Demo */}
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-orange-500/30">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-orange-500/20 rounded-lg px-3 py-1">
            <span className="text-orange-400 font-bold">STEP 3</span>
          </div>
        </div>
        <h3 className="text-2xl font-semibold text-orange-400 mb-3">Policy Checker</h3>
        <p className="text-gray-300 mb-6">
          Детальний policy звіт з рекомендаціями, action items та прикладами безпечних формулювань
        </p>
        <PolicyReportButton 
          variant="primary" 
          size="lg" 
          showDescription={false}
        />
      </div>

      {/* API Documentation */}
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-green-500/30">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-green-500/20 rounded-lg px-3 py-1">
            <span className="text-green-400 font-bold">API</span>
          </div>
        </div>
        <h3 className="text-2xl font-semibold text-green-400 mb-3">API Documentation</h3>
        <p className="text-gray-300 mb-6">
          Повна документація API з можливістю тестування всіх endpoints в реальному часі
        </p>
        <ApiDocsButton 
          variant="primary" 
          size="lg" 
          showDescription={false}
        />
      </div>
    </div>

    {/* Instructions */}
    <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-6 border border-blue-400/30 text-center">
      <p className="text-lg text-white font-semibold mb-2">
        🎯 Всі демо працюють в реальному часі
      </p>
      <p className="text-gray-300">
        Можете тестувати кожен етап workflow прямо зараз
      </p>
    </div>
  </div>
);

export const liveDemoSlideConfig = {
  title: "Живі демо",
  bg: "bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900"
};