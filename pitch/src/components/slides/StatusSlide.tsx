import React from 'react';

export const StatusSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Що вже працює?</h2>
    <div className="grid grid-cols-2 gap-6">
      <div className="space-y-4">
        <h3 className="text-3xl font-semibold text-green-400 mb-4">✅ Готово</h3>
        <div className="bg-green-500/20 rounded-xl p-6 border border-green-400/30">
          <h4 className="text-xl font-semibold text-white mb-2">Step 1: Pattern Mining</h4>
          <ul className="space-y-2 text-gray-300">
            <li>• Парсинг оголошень</li>
            <li>• Аналіз компонентів</li>
            <li>• HTML звіти з інсайтами</li>
          </ul>
        </div>
        <div className="bg-green-500/20 rounded-xl p-6 border border-green-400/30">
          <h4 className="text-xl font-semibold text-white mb-2">Step 2: Chat MVP Pro</h4>
          <ul className="space-y-2 text-gray-300">
            <li>• Conversational UI</li>
            <li>• Pattern suggestions</li>
            <li>• Platform presets</li>
            <li>• Session management</li>
          </ul>
        </div>
        <div className="bg-green-500/20 rounded-xl p-6 border border-green-400/30">
          <h4 className="text-xl font-semibold text-white mb-2">Step 3: Policy Checker</h4>
          <ul className="space-y-2 text-gray-300">
            <li>• Risk detection</li>
            <li>• Action items</li>
            <li>• HTML reports</li>
          </ul>
        </div>
      </div>
      <div className="space-y-4">
        <h3 className="text-3xl font-semibold text-blue-400 mb-4">🚧 В розробці</h3>
        <div className="bg-blue-500/20 rounded-xl p-6 border border-blue-400/30">
          <h4 className="text-xl font-semibold text-white mb-2">Video Generation</h4>
          <ul className="space-y-2 text-gray-300">
            <li>• TTS озвучка</li>
            <li>• FFmpeg монтаж</li>
            <li>• S3 upload</li>
          </ul>
        </div>
        <div className="bg-blue-500/20 rounded-xl p-6 border border-blue-400/30">
          <h4 className="text-xl font-semibold text-white mb-2">Global Patterns DB</h4>
          <ul className="space-y-2 text-gray-300">
            <li>• Семантичний пошук</li>
            <li>• Крос-кейсовий аналіз</li>
          </ul>
        </div>
        <div className="bg-blue-500/20 rounded-xl p-6 border border-blue-400/30">
          <h4 className="text-xl font-semibold text-white mb-2">Fix-it Automation</h4>
          <ul className="space-y-2 text-gray-300">
            <li>• Auto-rewrite VO</li>
            <li>• Auto re-render</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
);

export const statusSlideConfig = {
  title: "Поточний статус",
  bg: "bg-gradient-to-br from-teal-900 to-cyan-900"
};