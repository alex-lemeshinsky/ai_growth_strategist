import React from 'react';

export const CompetitiveSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Порівняння з ринком</h2>
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-white/20">
            <th className="pb-4 text-xl text-gray-400">Функція</th>
            <th className="pb-4 text-xl text-center text-gray-400">AdCreative.ai</th>
            <th className="pb-4 text-xl text-center text-gray-400">Pencil</th>
            <th className="pb-4 text-xl text-center text-green-400">AI Growth Strategist</th>
          </tr>
        </thead>
        <tbody className="text-lg">
          <tr className="border-b border-white/10">
            <td className="py-4 text-white">Генерація креативів</td>
            <td className="py-4 text-center text-green-400">✓</td>
            <td className="py-4 text-center text-green-400">✓</td>
            <td className="py-4 text-center text-green-400 font-bold">✓</td>
          </tr>
          <tr className="border-b border-white/10">
            <td className="py-4 text-white">Патерни з реальних ads</td>
            <td className="py-4 text-center text-red-400">✗</td>
            <td className="py-4 text-center text-yellow-400">~</td>
            <td className="py-4 text-center text-green-400 font-bold">✓</td>
          </tr>
          <tr className="border-b border-white/10">
            <td className="py-4 text-white">Policy Checker</td>
            <td className="py-4 text-center text-red-400">✗</td>
            <td className="py-4 text-center text-yellow-400">Basic</td>
            <td className="py-4 text-center text-green-400 font-bold">Advanced</td>
          </tr>
          <tr className="border-b border-white/10">
            <td className="py-4 text-white">Auto Fix-it</td>
            <td className="py-4 text-center text-red-400">✗</td>
            <td className="py-4 text-center text-red-400">✗</td>
            <td className="py-4 text-center text-green-400 font-bold">✓</td>
          </tr>
          <tr className="border-b border-white/10">
            <td className="py-4 text-white">Deep Analysis</td>
            <td className="py-4 text-center text-yellow-400">Basic</td>
            <td className="py-4 text-center text-yellow-400">Basic</td>
            <td className="py-4 text-center text-green-400 font-bold">Advanced</td>
          </tr>
          <tr>
            <td className="py-4 text-white">Platform optimization</td>
            <td className="py-4 text-center text-yellow-400">Manual</td>
            <td className="py-4 text-center text-green-400">✓</td>
            <td className="py-4 text-center text-green-400 font-bold">Auto</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div className="bg-gradient-to-r from-green-500/20 to-blue-500/20 rounded-xl p-6 border border-green-400/30">
      <p className="text-xl text-white font-semibold">
        Наша перевага: Повний end-to-end цикл від pattern mining до policy-safe креативів
      </p>
    </div>
  </div>
);

export const competitiveSlideConfig = {
  title: "Конкурентна позиція",
  bg: "bg-gradient-to-br from-red-900 to-pink-900"
};