import React from 'react';
import { Shield, Zap, CheckCircle, AlertTriangle } from 'lucide-react';
import { PolicyReportButton } from '../DemoButton';

export const PolicySlide = () => (
  <div className="space-y-6">
    <div className="bg-orange-500/20 rounded-xl p-2 inline-block">
      <span className="text-orange-400 font-bold text-xl px-4">STEP 3</span>
    </div>
    <h2 className="text-5xl font-bold text-white">Policy Checker + Рекомендації</h2>
    <div className="grid grid-cols-2 gap-6">
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-orange-500/30">
        <h3 className="text-2xl font-semibold text-orange-400 mb-4 flex items-center gap-3">
          <Shield className="w-7 h-7" />
          Перевірка ризиків
        </h3>
        <ul className="space-y-3 text-gray-300">
          <li className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            Health claims
          </li>
          <li className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            Бренди/логотипи
          </li>
          <li className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            Музичні права
          </li>
          <li className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            Чутливі теми
          </li>
          <li className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            Знаменитості
          </li>
          <li className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            NSFW контент
          </li>
        </ul>
      </div>
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-green-500/30">
        <h3 className="text-2xl font-semibold text-green-400 mb-4 flex items-center gap-3">
          <Zap className="w-7 h-7" />
          Smart Recommendations
        </h3>
        <div className="space-y-4 text-gray-300">
          <p className="text-lg">Детальні рекомендації для кожного ризику:</p>
          <div className="bg-red-500/20 p-3 rounded border-l-4 border-red-500">
            <p className="text-sm text-gray-400">❌ Ризик:</p>
            <p className="font-mono">"Повно лікує депресію"</p>
          </div>
          <div className="bg-green-500/20 p-3 rounded border-l-4 border-green-500">
            <p className="text-sm text-gray-400">✅ Рекомендація:</p>
            <p className="font-mono">"Може покращити настрій"</p>
          </div>
          <ul className="text-sm space-y-1 mt-4">
            <li>• Пояснення порушення</li>
            <li>• Приклади безпечних формулювань</li>
            <li>• Action items для виправлення</li>
          </ul>
        </div>
      </div>
    </div>
    <div className="bg-green-500/20 rounded-xl p-4 border border-green-400/30">
      <div className="flex items-center justify-between">
        <p className="text-lg text-white flex items-center gap-3">
          <CheckCircle className="w-6 h-6 text-green-400" />
          <span className="font-semibold">✅ Policy Checker реалізований та працює</span>
        </p>
        <PolicyReportButton 
          variant="secondary" 
          size="md" 
          showDescription={false}
        />
      </div>
    </div>
  </div>
);

export const policySlideConfig = {
  title: "Step 3: Policy Preflight",
  bg: "bg-gradient-to-br from-orange-900 to-red-900"
};